import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import matplotlib.pyplot as plot
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg #Puente entre matplotlib y tkinter, permite poner un gráfico dentro de tkinter
from graph import *
from node import Node

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

def CreateGraph_3(text):
    G=Graph()
    TextFile(G,text)
    return G

def ShowExampleGraph(): #Crea un gráfico de ejemplo
    global window_graph
    window_graph = CreateGraph_1()
    PlotGraph(window_graph)

def ShowCustomGraph(): #Crea un gráfico inventado
    global window_graph
    window_graph = CreateGraph_2()
    PlotGraph(window_graph)

def LoadGraph():
    global window_graph
    window_graph = CreateGraph_3("text")
    PlotGraph(window_graph)

def SelectNode(): #Muestra una ventana dónde escribir un nodo, busca el nodo en el gráfico y muestra sus vecinos y los dibuja en el gráfico
    global window_graph
    node_name=tk.simpledialog.askstring("Entry","Introduce the node name:",parent=root)
    node = Node("",0,0)
    neighbor_names = []
    for n in window_graph.nodes:
        if n.name == node_name:
            node = n
    if node != Node("",0,0):
        for neighbors in node.neighbors:
            neighbor_names.append(neighbors.name)
        tk.messagebox.showinfo("Neighbors",f"Neighbors of {node_name}:{','.join(neighbor_names)}")
    else:
        tk.messagebox.showinfo("Error","Node not found")


def PlotGraph(G): #Dibuja todos los segmentos y nodos, inserta el gráfico en el frame
    for widget in fig_frame.winfo_children():
        widget.destroy() #Esto elimina cualquier gráfico antes de poner otro, para evitar que se solapen
    fig,ax=plot.subplots(figsize=(6,6))
    ax.set_title("Graph Visualization")
    for node in G.nodes:
        ax.scatter(node.x,node.y,label=node.name,color='blue')
        ax.text(node.x,node.y,node.name,fontsize=12, ha='right')
    for segment in G.segments:
        ax.plot([segment.origin.x, segment.destination.x], [segment.origin.y, segment.destination.y], color='black')
        ax.annotate("",xy=(segment.destination.x, segment.destination.y),arrowprops=dict(arrowstyle="->", color='black', lw=1.5, mutation_scale=15))

    canvas= FigureCanvasTkAgg(fig,master=fig_frame) #Inserta el gráfico en tkinter
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

def AddNodeI(): #Permite añadir un nodo
    global window_graph
    name = simpledialog.askstring("New node", "Node name:", parent=root)
    x = float(simpledialog.askfloat("New node", "X-coordinate:", parent=root))
    y = float(simpledialog.askfloat("New node", "Y-coordinate:", parent=root))
    if name and x is not None and y is not None:
        node_nou = Node(name, x, y)
        AddNode(window_graph, node_nou)
        messagebox.showinfo("Éxito", f"Node '{name}' added.")
        PlotGraph(window_graph)
    else:
        messagebox.showwarning("Cancelled", "Node not added.")

'''def AddSegmentI():
    global window_graph
    name = simpledialog.askstring("New segment","Segment name",parent=root)
    origin_node=simpledialog.askstring("Origin node","Node name:",parent=root)
    destination_node = simpledialog.askstring("Destination node","Node name",parent=root)'''



#Algoritmo de Dijkastra para encontrar shortest path
def FindShortestPath():
    global window_graph

    start_name = simpledialog.askstring("Entrada", "Introduce el nodo de origen:", parent=root)
    end_name = simpledialog.askstring("Entrada", "Introduce el nodo de destino:", parent=root)

    start_node = next((n for n in window_graph.nodes if n.name == start_name), None)
    end_node = next((n for n in window_graph.nodes if n.name == end_name), None)

    if not start_node or not end_node:
        messagebox.showerror("Error", "Alguno de los nodos no existe.")
        return

    # Algoritmo de Dijkstra
    unvisited = {node: float('inf') for node in window_graph.nodes} #Distancias iniciales
    previous_nodes = {} #Almacena el nodo previo para reconstruir el camino más corto
    unvisited[start_node] = 0 #La distancia al nodo de inicio es 0
    visited = set() #Conjunto de nodos visitados

    while unvisited: #Obtener el nodo con la menor distancia no visitado
        current_node = min(unvisited, key=unvisited.get)
        current_distance = unvisited[current_node] #Si hemos alcanzado el nodo final podemos parar

        if current_node == end_node:
            break

        for segment in window_graph.segments: #Recorrer los segmentos adyacentes
            if segment.origin == current_node:
                neighbor = segment.destination
            elif segment.destination == current_node:
                neighbor = segment.origin
            else:
                continue

            if neighbor not in visited: #Si el nodo vecino no ha sido visitado o podemos mejorar la distancia
                new_distance = current_distance + segment.cost
                if new_distance < unvisited.get(neighbor, float('inf')): #Si encontramos una distancia más corta,actulizamos
                    unvisited[neighbor] = new_distance
                    previous_nodes[neighbor] = current_node

        visited.add(current_node) #Marcar el nodo actual como visitado
        unvisited.pop(current_node)

    # Reconstrucción del camino más corto
    path = []
    current = end_node
    while current != start_node:
        if current not in previous_nodes:
            messagebox.showinfo("Sin camino", "No hay un camino entre los nodos seleccionados.")
            return
        path.insert(0, current)
        current = previous_nodes[current]
    path.insert(0, start_node)

    # Mostrar el camino en un gráfico
    for widget in fig_frame.winfo_children():
        widget.destroy()

    fig, ax = plot.subplots(figsize=(6, 6)) #Dibujar el gráfico con el camino resaltado
    ax.set_title(f"Camino más corto de {start_name} a {end_name}")

    for node in window_graph.nodes: #Dibujar todos los nodos en gris, y los nodos del camino en azul
        color = 'blue' if node in path else 'gray'
        ax.scatter(node.x, node.y, color=color, s=100)
        ax.text(node.x, node.y, node.name, fontsize=12, ha='right')

    for segment in window_graph.segments:
        color = 'blue' if segment.origin in path and segment.destination in path else 'lightgray'
        ax.plot([segment.origin.x, segment.destination.x], [segment.origin.y, segment.destination.y], color=color, linewidth=3)

    canvas = FigureCanvasTkAgg(fig, master=fig_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Interfaz gráfica
window_graph = Graph()
root = tk.Tk()
root.title("Graph viewer")
root.geometry("800x800")

show_example_button = tk.Button(root, text="Show example graph", command=ShowExampleGraph)
show_example_button.pack(pady=10)

show_custom_button = tk.Button(root, text="Show invented graph", command=ShowCustomGraph)
show_custom_button.pack(pady=10)

load_file_button = tk.Button(root, text="Load graph from file", command=LoadGraph)
load_file_button.pack(pady=10)

select_node_button = tk.Button(root, text="Select nodes for neighbours", command=SelectNode)
select_node_button.pack(pady=10)

find_path_button = tk.Button(root, text="Shortest path between nodes", command=FindShortestPath)
find_path_button.pack(pady=10)

add_node_button = tk.Button(root,text="Add node",command=AddNodeI)
add_node_button.pack(pady=10)

fig_frame = tk.Frame(root)
fig_frame.pack(fill=tk.BOTH, expand=True)

root.mainloop()