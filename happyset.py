#Leitor de Grafo

import json
import cplex


def ler_grafo(u):
    arquive= open(u, 'r')
    conteudo= arquive.read()
    rawData = []
    def listar(x):
        for i in range(len(x)):
            if x[i]==' ' or x[i]=='\n':
                rawData.append(x[:i])
                listar(x[i+1:])
                break
    listar(conteudo)

    vertices, arestas = [int(v) for v in rawData[:2]]
    edgeData = [json.loads(edge) for edge in rawData[2:]]
    print(str(vertices) + ' vertices, ' + str(arestas) + ' arestas, ')

    m1, m2 = [], []
    for i in range(vertices):
        m1.append([0]*vertices)
        m2.append([])

    def setupM1(y):
        if len(y) != 0:
            m1[y[0]][y[1]] = 1
            m1[y[1]][y[0]] = 1
            setupM1(y[2:])
    setupM1(edgeData)
    
    if len(m1) != 0:
        for i in  range(len(m1)):
            for j in range(len(m1[i])):
                if m1[i][j] == 1:
                    m2[i].append(j+1)
    # print(m1, m2)
    return m1,m2,vertices,arestas


def resolve_modelo(m1,m2,vertices,arestas,k):
    cpx = cplex.Cplex()

    y = cpx.variables.add(obj=[0] * vertices,
                             lb=[0] * vertices, ub=[1] * vertices,
                             types=['B'] * vertices,
                             names=['y_%d' % (p) for p in range(1,vertices+1)])
    h = cpx.variables.add(obj=[1] * vertices,
                            lb=[0] * vertices, ub=[1] * vertices,
                            types=['B'] * vertices,
                            names=['h_%d' % (z) for z in range(1,vertices+1)])



    #Restrição 2
    cpx.linear_constraints.add(
        lin_expr=[cplex.SparsePair([y[i] for i in range(vertices)], [1.0]*vertices)],
        senses=['E'],
        rhs= [k])


    #Restrição 3
    cpx.linear_constraints.add(
        lin_expr=[cplex.SparsePair([h[i]]+[y[i]], [1.0,-1.0])
                  for i in range(vertices)],
        senses=['L'] * vertices,
        rhs=[0.0] * vertices)
    
    
    #Restrição 4
    cpx.linear_constraints.add(
        lin_expr=[cplex.SparsePair([h[i]]+[y[j-1]], [1.0,-1.0])
                  for i in range(vertices) for j in m2[i]],
        senses=['L'] * (arestas*2),
        rhs=[0.0] * (arestas*2))
    
    
    #Restrição 5
    cpx.linear_constraints.add(
        lin_expr=[cplex.SparsePair([h[i]]+[y[i]]+[y[j-1] for j in m2[i]], [1.0,-1.0]+[-1.0]*len(m2[i]))
                  for i in range(vertices)],
        senses=['G'] * vertices,
        rhs=[-len(m2[i]) for i in range(vertices)])

    
    cpx.parameters.threads.set(1)
    cpx.objective.set_sense(cpx.objective.sense.maximize)
    
    cpx.write('model.lp')
    cpx.solve()

    print('Solution status:                   %d' % cpx.solution.get_status())
    print('Nodes processed:                   %d' %
          cpx.solution.progress.get_num_nodes_processed())
    print('Active user cuts/lazy constraints: %d' %
          cpx.solution.MIP.get_num_cuts(cpx.solution.MIP.cut_type.user))
    tol = cpx.parameters.mip.tolerances.integrality.get()
    print('Optimal value:                     %f' %
          cpx.solution.get_objective_value())
    values = cpx.solution.get_values()
    for j in [x for x in list(range(vertices)) if values[y[x]] >= 1 - tol]:
        print('Vertice', str(j), 'foi escolhido e', str(j), end= ' ')
        print('está feliz' if (values[h[j]] >= 1 - tol) else 'não está feliz') 
        
def getFileName(nome):
    if nome == '':
        return 'grafo.txt'
    elif nome[-4:] == '.txt':
        return nome
    else:
        return nome + '.txt'

def getK():
    k = input('k (Enter 4 default):')
    if k == '':
        return 3
    return int(k)

def main():
    filename = getFileName(input('Nome do arquivo .txt contendo o grafo (Enter 4 default):'))
    k = getK()
    m1,m2,vertices,arestas= ler_grafo(filename)
    resolve_modelo(m1,m2,vertices,arestas,k)

if __name__ == "__main__":
    main()

