import matplotlib.pyplot as plot
from graph import *
def CreateGraph_1 ():
    G = Graph()

    AddNode(G, Node("A", 1, 20))
    AddNode(G, Node("B", 8, 17))
    AddNode(G, Node("C", 15, 20))
    AddNode(G, Node("D", 18, 15))
    AddNode(G, Node("E", 2, 4))
    AddNode(G, Node("F", 6, 5))
    AddNode(G, Node("G", 12, 12))
    AddNode(G, Node("H", 10, 3))
    AddNode(G, Node("I", 19, 1))
    AddNode(G, Node("J", 13, 5))
    AddNode(G, Node("K", 3, 15))
    AddNode(G, Node("L", 4, 10))

    AddSegment(G, "A", "B")
    AddSegment(G, "A", "E")
    AddSegment(G, "A", "K")
    AddSegment(G, "B", "A")
    AddSegment(G, "B", "C")
    AddSegment(G, "B", "F")
    AddSegment(G, "B", "K")
    AddSegment(G, "B", "G")
    AddSegment(G, "C", "D")
    AddSegment(G, "C", "G")
    AddSegment(G, "D", "G")
    AddSegment(G, "D", "H")
    AddSegment(G, "D", "I")
    AddSegment(G, "E", "F")
    AddSegment(G, "F", "L")
    AddSegment(G, "G", "B")
    AddSegment(G, "G", "F")
    AddSegment(G, "G", "H")
    AddSegment(G, "I", "D")
    AddSegment(G, "I", "J")
    AddSegment(G, "J", "I")
    AddSegment(G, "K", "A")
    AddSegment(G, "K", "L")
    AddSegment(G, "L", "K")
    AddSegment(G, "L", "F")

    return G

print ("Trying the graph")
G = CreateGraph_1 ()
n = GetClosest(G,15,5)
print (n.name) # La respuesta debe ser J
n = GetClosest(G,8,19)
print (n.name) # La respuesta debe ser B
PlotNode(G, "C")
Plot(G)

def CreateGraph_2():
    G = Graph()

    AddNode(G, Node("MAD", 5, 14))
    AddNode(G, Node("BCN", 8, 17))
    AddNode(G, Node("SEV", 1, 2))
    AddNode(G, Node("VCN", 11, 11))
    AddNode(G, Node("STC", 24, 14))
    AddNode(G, Node("PMA", 20, 4))

    AddSegment(G, "MAD", "BCN")
    AddSegment(G, "MAD", "SEV")
    AddSegment(G, "PMA", "STC")
    AddSegment(G, "VCN", "BCN")
    AddSegment(G, "BCN", "STC")
    AddSegment(G, "STC", "SEV")
    AddSegment(G, "SEV", "VCN")
    AddSegment(G, "SEV", "BCN")
    AddSegment(G, "PMA", "BCN")

    return G
G = CreateGraph_2()
n = GetClosest(G,6,13)
print(n.name) #La respuesta debe ser MAD
n = GetClosest(G,2,3)
print(n.name) #La respuesta es PMA
Plot(G)
PlotNode(G,"BCN")












