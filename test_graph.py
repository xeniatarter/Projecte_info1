import matplotlib.pyplot as plot
from graph import *
from node import Node

def test_CreateGraph_1():
    G = CreateGraph_1()
    n = GetClosest(G, 15, 5)
    print(n.name)  # Respuesta J
    n = GetClosest(G, 8, 19)
    print(n.name)  # Respuesta B
    PlotNode(G, "C")
    Plot(G)

def test_CreateGraph_2():
    G = CreateGraph_2()
    n = GetClosest(G, 6, 13)
    print(n.name)  # Respuesta MAD
    n = GetClosest(G, 2, 3)
    print(n.name)  # Respuesta: PMA
    Plot(G)
    PlotNode(G, "BCN")

def test_CreateGraph_3():
    G = CreateGraph_3()
    n = GetClosest(G, 12, 2)
    print(n.name)  # Respuesta: Z
    n = GetClosest(G, 3, 6)
    print(n.name)  # Respuesta: T
    Plot(G)
    PlotNode(G, "X")


test_CreateGraph_1()
test_CreateGraph_2()
test_CreateGraph_3()

