import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from graph import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg #Puente entre matplotlib y tkinter, permite poner un gráfico dentro de tkinter
from path import find_shortest_path
from node import Node
import matplotlib.pyplot as plot

def ShowExampleGraph():
    global window_graph
    window_graph = CreateGraph_1()  # Llamamos a CreateGraph_1 desde graph.py
    PlotGraph(window_graph)

def ShowCustomGraph():
    global window_graph
    window_graph = CreateGraph_2()  # Llamamos a CreateGraph_2 desde graph.py
    PlotGraph(window_graph)

def LoadGraph():
    global window_graph
    window_graph = CreateGraph_3("text")  # Llamamos a CreateGraph_3 desde graph.py (si existe)
    PlotGraph(window_graph)

def SelectNode():
    global window_graph
    node_name = simpledialog.askstring("Entry", "Introduce the node name:", parent=root)
    neighbors = GetNeighbors(window_graph, node_name)

    if neighbors:
        neighbor_names = [n.name for n in neighbors]
        messagebox.showinfo("Neighbors", f"Neighbors of {node_name}: {', '.join(neighbor_names)}")
    else:
        messagebox.showerror("Error", "Node not found or has no neighbors.")

def PlotGraph(G):
    for widget in fig_frame.winfo_children():
        widget.destroy()  # Elimina cualquier gráfico anterior
    fig, ax = plot.subplots(figsize=(6, 6))
    ax.set_title("Graph Visualization")
    for node in G.nodes:
        ax.scatter(node.x, node.y, label=node.name, color='blue')
        ax.text(node.x, node.y, node.name, fontsize=12, ha='right', color='red')
    for segment in G.segments:
        ax.plot([segment.origin.x, segment.destination.x], [segment.origin.y, segment.destination.y], color='black')
        ax.annotate("", xy=(segment.destination.x, segment.destination.y), xytext=(segment.origin.x, segment.origin.y), arrowprops=dict(arrowstyle="->", color='black', lw=1.5, mutation_scale=15))
    ax.set_aspect('equal')
    canvas = FigureCanvasTkAgg(fig, master=fig_frame)  # Inserta el gráfico en tkinter
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

def AddNodeInterface():
    global window_graph
    name = simpledialog.askstring("New node", "Node name:", parent=root)
    x = simpledialog.askfloat("New node", "X-coordinate:", parent=root)
    y = simpledialog.askfloat("New node", "Y-coordinate:", parent=root)

    if name and x is not None and y is not None:
        node_nou = Node(name, x, y)
        AddNode(window_graph, node_nou)
        messagebox.showinfo("Success", f"Node '{name}' added.")
        PlotGraph(window_graph)
    else:
        messagebox.showwarning("Cancelled", "Node not added.")

def AddSegmentInterface():
    global window_graph
    origin_node = simpledialog.askstring("New segment", "Origin node:", parent=root)
    destination_node = simpledialog.askstring("New segment", "Destination node:", parent=root)

    if origin_node and destination_node:
        if AddSegment(window_graph, origin_node, destination_node):
            messagebox.showinfo("Success", f"Segment from '{origin_node}' to '{destination_node}' added.")
        else:
            messagebox.showerror("Error", "Failed to add the segment.")
        PlotGraph(window_graph)
    else:
        messagebox.showwarning("Cancelled", "Segment not added.")


# Función para encontrar el camino más corto, delegando en path.py
def FindShortestPath():
    global window_graph
    start_name = simpledialog.askstring("Find path", "Origin node:", parent=root)
    end_name = simpledialog.askstring("Find path", "Destination node:", parent=root)
    path = find_shortest_path(window_graph, start_name, end_name)  # Delegamos en path.py

    if not path:
        messagebox.showinfo("Without path", "There is no path between the selected nodes")
        return

    # Mostrar el camino en un gráfico
    for widget in fig_frame.winfo_children():
        widget.destroy()

    fig, ax = plot.subplots(figsize=(6, 6))  # Dibujar el gráfico con el camino resaltado
    ax.set_title(f"Shortest path from {start_name} to {end_name}")

    path_node_names = [n.name for n in path]
    for node in window_graph.nodes:
        color = 'blue' if node.name in path_node_names else 'gray'
        ax.scatter(node.x, node.y, color=color, s=100)
        ax.text(node.x, node.y, node.name, fontsize=12, ha='right')

    # Mostrar todos los segmentos
    for segment in window_graph.segments:
        if segment.origin in path and segment.destination in path:
            try:
                # Verificamos si es parte directa del camino
                idx = path.index(segment.origin)
                if path[idx + 1] == segment.destination:
                    color = 'blue'
                    lw = 3
                else:
                    color = 'lightgray'
                    lw = 1
            except (ValueError, IndexError):
                color = 'lightgray'
                lw = 1
        else:
            color = 'lightgray'
            lw = 1

        # Dibujar flecha
        ax.annotate("",xy=(segment.destination.x, segment.destination.y),xytext=(segment.origin.x, segment.origin.y),arrowprops=dict(arrowstyle="->", color=color, lw=lw, mutation_scale=15))
    ax.set_aspect('equal')
    canvas = FigureCanvasTkAgg(fig, master=fig_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


# Interfaz gráfica
window_graph = Graph()
root = tk.Tk()
root.title("Graph viewer")
root.geometry("1000x600")  # Cambié el tamaño para dar más espacio al gráfico

# Crear un frame para los botones
button_frame = tk.Frame(root, width=250)  # Frame de botones, especificamos un tamaño fijo
button_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)  # Coloca los botones a la izquierda

# Crear un frame para el gráfico
fig_frame = tk.Frame(root)
fig_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)  # Coloca el gráfico a la derecha

# Botones de la interfaz (en el frame de botones)
show_example_button = tk.Button(button_frame, text="Show example graph", command=ShowExampleGraph)
show_example_button.pack(pady=10)

show_custom_button = tk.Button(button_frame, text="Show invented graph", command=ShowCustomGraph)
show_custom_button.pack(pady=10)

load_file_button = tk.Button(button_frame, text="Load graph from file", command=LoadGraph)
load_file_button.pack(pady=10)

select_node_button = tk.Button(button_frame, text="Select nodes for neighbours", command=SelectNode)
select_node_button.pack(pady=10)

find_path_button = tk.Button(button_frame, text="Shortest path between nodes", command=FindShortestPath)
find_path_button.pack(pady=10)

add_node_button = tk.Button(button_frame, text="Add node", command=AddNodeInterface)
add_node_button.pack(pady=10)

add_segment_button = tk.Button(button_frame, text="Add segment", command=AddSegmentInterface)
add_segment_button.pack(pady=10)

root.mainloop()

