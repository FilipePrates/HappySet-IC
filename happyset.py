import json
import cplex

def listar(x):
    rawData = []
    start = 0
    for i in range(len(x)):
        if x[i] == ' ' or x[i] == '\n':
            rawData.append(x[start:i])
            start = i + 1
    return rawData


def ler_grafo(u):
    arquive = open(u, 'r')
    content = arquive.read()
    rawData = []
    rawData = listar(content)

    vertices, arestas = [int(v) for v in rawData[:2]]
    edgeData = [json.loads(edge) for edge in rawData[2:]]
    print(str(vertices) + ' vertices, ' + str(arestas) + ' arestas, ')

    m1, m2 = [], []
    for i in range(vertices):
        m1.append([0]*vertices)
        m2.append([])
    
    for i in range(0,len(edgeData)-1):
        m1[edgeData[i]][edgeData[i+1]] = 1
        m1[edgeData[i+1]][edgeData[i]] = 1
        i += 1

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
    # limite de tempo de clock ~1h processamento CPU
    cpx.objective.set_sense(cpx.objective.sense.maximize)
    
    cpx.write('model.lp')
    # begin time meu
    cpx.solve()
    # end time meu
    print(cpx.solution)
    # limtie inf, sup. inf == sup => otimo
    print('Solution status:                   %d' % cpx.solution.get_status())
    # se não otimo => best bound, best solution
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
    # relaxação linear
def main():
    graphClass = input('Classe do grafo? (Enter 4 default):')
    if graphClass == '':
        graphClass = 'star'
    graphSize = input('Tamanho do grafo? (n = 2^x):')
    if graphSize == '':
        graphSize = '1024'
    k = input('k (Enter 4 default):')
    if k == '':
        k = 3
    filename = f'graphs/{graphClass}/{graphClass}_{graphSize}.txt'
    m1,m2,vertices,arestas= ler_grafo(filename)
    resolve_modelo(m1,m2,vertices,arestas,int(k))

if __name__ == "__main__":
    main()

#   Default:
# Nome do arquivo .txt contendo o grafo (Enter 4 default):
# k (Enter 4 default):
# 4 vertices, 3 arestas, 
# Default row names c1, c2 ... being created.
# Version identifier: 22.1.1.0 | 2022-11-28 | 9160aff4d
# CPXPARAM_Read_DataCheck                          1
# CPXPARAM_Threads                                 1
# Tried aggregator 1 time.
# MIP Presolve eliminated 8 rows and 1 columns.
# MIP Presolve modified 8 coefficients.
# Reduced MIP has 7 rows, 7 columns, and 22 nonzeros.
# Reduced MIP has 7 binaries, 0 generals, 0 SOSs, and 0 indicators.
# Presolve time = 0.00 sec. (0.03 ticks)
# Found incumbent of value 2.000000 after 0.00 sec. (0.04 ticks)
# Probing time = 0.00 sec. (0.01 ticks)
# Tried aggregator 1 time.
# Detecting symmetries...
# MIP Presolve eliminated 3 rows and 0 columns.
# Reduced MIP has 4 rows, 7 columns, and 13 nonzeros.
# Reduced MIP has 7 binaries, 0 generals, 0 SOSs, and 0 indicators.
# Presolve time = 0.00 sec. (0.01 ticks)
# Probing time = 0.00 sec. (0.00 ticks)
# Clique table members: 7.
# MIP emphasis: balance optimality and feasibility.
# MIP search method: dynamic search.
# Parallel mode: none, using 1 thread.
# Root relaxation solution time = 0.00 sec. (0.00 ticks)

#         Nodes                                         Cuts/
#    Node  Left     Objective  IInf  Best Integer    Best Bound    ItCnt     Gap

# *     0+    0                            2.0000        3.0000            50.00%
#       0     0        cutoff              2.0000                      1     --- 

# Root node processing (before b&c):
#   Real time             =    0.00 sec. (0.08 ticks)
# Sequential b&c:
#   Real time             =    0.00 sec. (0.00 ticks)
#                           ------------
# Total (root+branch&cut) =    0.00 sec. (0.08 ticks)
# Solution status:                   101
# Nodes processed:                   0
# Active user cuts/lazy constraints: 0
# Optimal value:                     2.000000
# Vertice 0 foi escolhido e 0 não está feliz
# Vertice 1 foi escolhido e 1 está feliz
# Vertice 2 foi escolhido e 2 está feliz
