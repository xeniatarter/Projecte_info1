import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import json
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Graph:
    def __init__(self, root):
        self.root = root
        self.root.title("Graph Thingy")

        self.graph = {}

        # Buttons to do graphy stuff
        tk.Button(root, text="Show Example Graph", command=self.show_example_graph).pack(pady=5)
        tk.Button(root, text="Show My Cool Graph", command=self.show_custom_graph).pack(pady=5)
        tk.Button(root, text="Load Graph from File", command=self.load_graph_from_file).pack(pady=5)
        tk.Button(root, text="Find Node Buddies", command=self.show_neighbors).pack(pady=5)

        # Place for drawing the graph
        self.canvas_frame = tk.Frame(root)
        self.canvas_frame.pack()

        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.canvas_frame)
        self.canvas.get_tk_widget().pack()

    def draw_graph(self):
        self.ax.clear()
        self.ax.set_xlim(-1, 1)
        self.ax.set_ylim(-1, 1)

        pos = {}
        angle = 0
        step = 360 / len(self.graph) if self.graph else 1
        for node in self.graph:
            pos[node] = (0.8 * plt.cos(angle), 0.8 * plt.sin(angle))
            angle += step

        for node, edges in self.graph.items():
            x, y = pos[node]
            self.ax.text(x, y, str(node), fontsize=12, ha='center', va='center',
                         bbox=dict(facecolor='lightblue', edgecolor='black', boxstyle='circle'))
            for neighbor in edges:
                nx, ny = pos.get(neighbor, (0, 0))
                self.ax.plot([x, nx], [y, ny], 'gray')

        self.canvas.draw()

    def show_example_graph(self):
        self.graph = {1: [2, 4], 2: [1, 3, 4], 3: [2, 4], 4: [1, 2, 3]}
        self.draw_graph()

    def show_custom_graph(self):
        self.graph = {"A": ["B", "C"], "B": ["A", "D"], "C": ["A", "D"], "D": ["B", "C"]}
        self.draw_graph()

    def load_graph_from_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        if not file_path:
            return
        try:
            with open(file_path, "r") as file:
                data = json.load(file)
                self.graph = data.get("graph", {})
                self.draw_graph()
        except Exception as e:
            messagebox.showerror("Oops", f"Couldn't load file: {e}")

    def show_neighbors(self):
        node = simpledialog.askstring("Yo", "Which node you wanna check?")
        if node in self.graph:
            neighbors = self.graph[node]
            messagebox.showinfo("Buddies", f"Neighbors of {node}: {', '.join(map(str, neighbors))}")
        else:
            messagebox.showerror("Uh-oh", "That node ain't here.")


if __name__ == "__main__":
    root = tk.Tk()
    app = Graph(root)
    root.mainloop()

