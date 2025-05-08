from node import Node
from segment import Segment
import matplotlib.pyplot as plot

class Graph:
    def __init__(self):
        self.nodes = []
        self.segments = []

def GetClosest(g, x, y):  # Busca el nodo más cercano a una posición dada en el gráfico
    return min(g.nodes, key=lambda node: Node.Distance(node, Node("temp", x, y)))  # Busca el nodo con la menor distancia

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


def CreateGraph_3(filename):
    G = Graph()
    TextFile(G, filename)
    return G


def AddNode (g,n):
    if n in g.nodes:
        return False
    g.nodes.append(n)
    return True

def AddSegment(g, OriginNode, DestinationNode):
    origin = next((node for node in g.nodes if node.name == OriginNode), None) #Next busca el primer elemento que cumpla con la condición indicada
    destination = next((node for node in g.nodes if node.name == DestinationNode), None) #None es la respuesta que recibiremos si no se encuentra ningún nodo que cumpla las condiciones
    if not origin or not destination:
        return False
    segment = Segment(f"{OriginNode}-{DestinationNode}", origin, destination,color='black')
    g.segments.append(segment)
    origin.AddNeighbor(destination) #Afegim el nodo destino a la llista de veïns del node origin
    return True

def GetClosest(g,x,y): #Busca el nodo más cercano a una posición dada en el gráfico
    return min(g.nodes, key=lambda node: Node.Distance(node, Node("temp",x,y))) #Min encuentra el nodo con menor distancia al punto
    #key=lambda es una pequeña función que devuelve el valor entre un nodo y un punto (x,y)
    #Node("temp",x,y) crea un nodo temporal que se llama temp y está en x,y y se usa para comparar la distancia entre los nodos y este nodo temporal.

def GetNeighbors(graph, node_name):
    for node in graph.nodes:
        if node.name == node_name:
            return node.neighbors
    return None

def Plot(g):
    plot.figure() #Crea un espai blanc on nosaltres podem entrar les dades y fer el plot que vulguem
    for segment in g.segments:
        x_values = [segment.origin.x,segment.destination.x] #origin ve de class segment, x ve de class node i segment ve de AddSegment
        y_values = [segment.origin.y,segment.destination.y]
        plot.plot(x_values,y_values,color='green',linestyle='solid',linewidth=2)
        mid_x = (segment.origin.x+segment.destination.x)/2
        mid_y = (segment.origin.y+segment.destination.y)/2
        plot.text(mid_x,mid_y,f"{segment.cost:.2f}",fontsize=10,ha='center') #2f nos da dos decimales solo, ha nos dice dónde se alinea el texto respecto la coordenada (x,y)
    for node in g.nodes:
        plot.scatter(node.x,node.y,color='blue',s=100)
        plot.text(node.x +0.4,node.y +0.25,node.name,color = 'red', fontweight='bold',fontsize=10,ha='center')
    plot.show()

def PlotNode (g,NameOrigin):
    origin=next((node for node in g.nodes if node.name==NameOrigin),None)
    if not origin:
        return False
    plot.figure()
    for segment in g.segments: #Buscamos entre los segmentos que hay en la lista de g.segments
       if segment.origin==origin:
            x_values=[segment.origin.x,segment.destination.x]
            y_values=[segment.origin.y,segment.destination.y]
            #color = 'red' if segment.origin==origin else 'black' #Si el segmento parte del nodo de orgien será rojo sino negro.
            plot.plot(x_values,y_values,color='red',lw=2)
            mid_x = (segment.origin.x + segment.destination.x) / 2
            mid_y = (segment.origin.y + segment.destination.y) / 2
            plot.text(mid_x, mid_y, f"{segment.cost:.2f}", fontsize=10, ha='center')
    for node in g.nodes: #Buscamos entre los nodos que hay en la lista de g.nodes

        if node == origin:
            color = 'blue'
        elif node in origin.neighbors:
            color = 'green'
        else:
            color = 'gray'
        plot.scatter(node.x,node.y,color = color,s=100)
        plot.text(node.x,node.y,node.name,fontsize=10, ha='center')
    plot.show()
    return True

def TextFile (g,text):
    with open(text,'r') as file:
        lines = file.readlines()
    file.close()

    section = None #De momento no estamos en ninguna sección
    for line in lines: #Coge una línea una a una y la guarda en la variable line
        line = line.strip()
        if line == "NODES":
            section = "Nodes"
            continue  #Salta a la siguiente vuelta del bucle, ignora el resto de código dentro el bucle
        elif line == "SEGMENTS":
            section = "Segments"
            continue
        if not line:
            continue

        if section == 'Nodes':
            name, x, y = line.split(",")
            g.nodes.append(Node(name, float(x),float(y)))
        elif section == 'Segments':
            origin, destination = line.split(",")
            AddSegment(g, origin, destination)