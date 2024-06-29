import itertools
import random
import networkx as nx
import numpy as np
from random import choice
from more_itertools import random_product

directory = "/home/cliente/Code/UFRJ/HappySet-IC"

def rand_sample(all):
    sample = choice(all)
    all.remove(sample)
    return sample

def generateStarGraphs():
    for n in range(1,16):
        f = open(f"{directory}/graphs/star/star_" + str(2**n) + ".txt", "w") 
        f.write(str(2**n) + " " + str(2**n - 1) + "\n")    # Write inside file 
        for e in range(1, 2**n):
            # print("2**n:", 2**n, "e:", e)
            f.write("0 " + str(e) + "\n")    # Write inside file 
        f.write("end")
        f.close() 

def generateBipartiteGraphs():
    for n in range(1,16):
        f = open(f"{directory}/graphs/bipartite/bipartite_" + str(2**n) + ".txt", "w")
        num_vertices = 2**n
        set_A_size = 2**(n-1)
        set_B_size = 2**(n-1)
        num_edges = set_A_size * set_B_size
        f.write(f"{num_vertices} {num_edges}\n")
        set_A = range(set_A_size)
        set_B = range(set_A_size, num_vertices)
        # Write all edges. Each vertex in set A connects to every vertex in set B
        for a, b in itertools.product(set_A, set_B):
            f.write(f"{a} {b}\n")
        f.write("end")
        f.close()

def generateRandomBipartiteGraphs():
    for n in range(1, 16):
        with open(f"{directory}/graphs/bipartite_random/bipartite_" + str(2**n) + ".txt", "w") as f:
            num_vertices = 2**n
            set_size = 2**(n-1)
            p = 0.5  # Probability of each edge existing
            edges = []
            set_A = range(set_size)
            set_B = range(set_size, num_vertices)
            for a, b in itertools.product(set_A, set_B):
                if random.random() < p:
                    edges.append((a, b))
            num_edges = len(edges)
            f.write(f"{num_vertices} {num_edges}\n")
            for edge in edges:
                f.write(f"{edge[0]} {edge[1]}\n")
            f.write("end")

def generateCubicGraphs():
    for n in range(1, 16):
        f = open(f"{directory}/graphs/cubic/cubic_{2**n}.txt", "w")
        num_vertices = 2**n
        num_edges = num_vertices * 3 // 2  # Cubic graph has 3*d/2 edges where d is the number of vertices (approximately)
        f.write(f"{num_vertices} {num_edges}\n")
        for i in range(num_vertices):
            neighbors = [(i - 1) % num_vertices, (i + 1) % num_vertices, (i + num_vertices // 2) % num_vertices]  # Connect each vertex to 3 neighbors
            for neighbor in neighbors:
                f.write(f"{i} {neighbor}\n")
        f.write("end")
        f.close()

def generateBAGraphs():
    for n in range(2, 16):
        num_vertices = 2**n
        m = 2  # Number of edges to attach from a new node to existing nodes
        G = nx.barabasi_albert_graph(num_vertices, m)
        with open(f"{directory}/graphs/BA/BA_" + str(num_vertices) + ".txt", "w") as f:
            num_edges = G.number_of_edges()
            f.write(f"{num_vertices} {num_edges}\n")
            for edge in G.edges():
                f.write(f"{edge[0]} {edge[1]}\n")
            f.write("end")

def generateLollipopGraphs():
    for n in range(2, 16):
        m = 2**(n-1)  # Size of the complete part
        t = 2**(n-1)  # Length of the path part
        G = nx.lollipop_graph(m, t)
        num_vertices = G.number_of_nodes()
        with open(f"{directory}/graphs/lollipop/lollipop_" + str(num_vertices) + ".txt", "w") as f:
            num_edges = G.number_of_edges()
            f.write(f"{num_vertices} {num_edges}\n")
            for edge in G.edges():
                f.write(f"{edge[0]} {edge[1]}\n")
            f.write("end")
def main():
    graphType = input('Gerar qual grafo?')
    if graphType == 'star':
        generateStarGraphs()
    if graphType == 'bipartite':
        generateBipartiteGraphs()
    if graphType == 'bipartite_rand':
        generateRandomBipartiteGraphs()
    if graphType == 'cubic':
        generateCubicGraphs()
    if graphType == 'BA':
        generateBAGraphs()
    if graphType == 'lollipop':
        generateLollipopGraphs()
        
if __name__ == "__main__":
    main()
