import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox, ttk
from graph import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg #Puente entre matplotlib y tkinter, permite poner un gráfico dentro de tkinter
from matplotlib.widgets import Cursor
from matplotlib.patches import FancyArrowPatch
from matplotlib.backend_bases import key_press_handler #Es para que reaccione al ratón
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
from path import find_shortest_path
from node import Node
import matplotlib.pyplot as plot
from airspace import AirSpace, CreateGraph4, AddNavPoint, AddAirport, AddNavSegment
from navpoints import NavPoint
from navsegments import NavSegment
from navairports import NavAirport
from PIL import Image, ImageTk
import simplekml
import requests



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


def SelectNode(): #Nos da pintados de otro color los nodos vecinos y los segmentos que los une
    global window_graph
    node_name = simpledialog.askstring("Entry", "Introduce the node name:", parent=root)
    neighbors = GetNeighbors(window_graph, node_name)

    if not neighbors:
        messagebox.showerror("Error", f"No neighbors found for node '{node_name}'.")
        return

    neighbor_names = [n.name for n in neighbors]
    messagebox.showinfo("Neighbors", f"Neighbors of {node_name}: {', '.join(neighbor_names)}")

    for widget in fig_frame.winfo_children():
        widget.destroy()

    fig, ax = plot.subplots(figsize=(6, 6))
    ax.set_title(f"Neighbors of {node_name}")

    for node in window_graph.nodes:
        if node.name == node_name:
            color = 'blue'
        elif node in neighbors:
            color = 'lightskyblue'
        else:
            color = 'lightgray'
        ax.scatter(node.x, node.y, color=color, s=100)
        txt = ax.text(node.x, node.y, node.name, fontsize=12, ha='right', clip_on=True)

    for segment in window_graph.segments:
        if (segment.origin.name == node_name and segment.destination in neighbors) or (segment.destination.name == node_name and segment.origin in neighbors):
            seg_color = 'lightskyblue'
            lw = 2
        else:
            seg_color = 'lightgray'
            lw = 1

        arrow = FancyArrowPatch((segment.origin.x, segment.origin.y),(segment.destination.x, segment.destination.y),arrowstyle='->',color=seg_color,mutation_scale=15,lw=lw,clip_on=True)
        ax.add_patch(arrow)

    ax.set_aspect('equal', adjustable='box')
    ZoomGraph(fig, ax, fig_frame)


def PlotGraph(G): #Dibuja los nodos y segmentos, si se trata de un SID o STAR los pone de otro color
    for widget in fig_frame.winfo_children():
        widget.destroy() #Elimina cualquier gráfico anterior

    fig, ax = plot.subplots(figsize=(6, 6))
    ax.set_title("Graph Visualization")

    for node in G.nodes:
        #Oculta SIDs o STARs si está desmarcado en el botón
        if node.name.endswith('.D') and not show_sids.get():
            continue
        if node.name.endswith('.A') and not show_stars.get():
            continue
        if node.name.endswith('.D'):
            color = 'springgreen'
        elif node.name.endswith('.A'):
            color = 'fuchsia'
        else:
            color = 'blue'

        ax.scatter(node.x, node.y, color=color)
        if show_nodes.get():
            txt = ax.text(node.x + 0.1, node.y + 0.1, node.name, fontsize=8, ha='right', color='purple')
            txt.set_clip_on(True)


    for segment in G.segments:
        # Si el origen o destino es SID/STAR y está oculto, no dibujar el segmento
        if (segment.origin.name.endswith('.D') and not show_sids.get()) or \
                (segment.origin.name.endswith('.A') and not show_stars.get()) or \
                (segment.destination.name.endswith('.D') and not show_sids.get()) or \
                (segment.destination.name.endswith('.A') and not show_stars.get()):
            continue

        arrow = FancyArrowPatch((segment.origin.x, segment.origin.y), (segment.destination.x, segment.destination.y),
                                arrowstyle='->', color='black', mutation_scale=15, lw=1.5, clip_on=True)
        ax.add_patch(arrow)
        if show_distance.get():  # Calculamos distancia Eucaldiana
            dx = segment.destination.x - segment.origin.x
            dy = segment.destination.y - segment.origin.y
            distance = round((dx ** 2 + dy ** 2) ** 0.5, 2)  # Redondea a solo dos decimales
            mid_x = (segment.origin.x + segment.destination.x) / 2
            mid_y = (segment.origin.y + segment.destination.y) / 2
            dist_txt = ax.text(mid_x, mid_y, f"{distance:.2f}", fontsize=8, color='red', ha='center', va='center')
            dist_txt.set_clip_on(True)



    ax.set_aspect('equal', adjustable='box')
    ZoomGraph(fig, ax, fig_frame)


def ZoomGraph(fig, ax, parent_frame): #Permite hacer zoom a los gráficos
    canvas = FigureCanvasTkAgg(fig, master=parent_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    canvas.mpl_connect('button_press_event', Click)
    toolbar = NavigationToolbar2Tk(canvas, parent_frame)
    toolbar.update()
    toolbar.pack(side=tk.BOTTOM, fill=tk.X)

    def on_scroll(event):
        cur_xlim = ax.get_xlim()
        cur_ylim = ax.get_ylim()
        xdata, ydata = event.xdata, event.ydata
        if xdata is None or ydata is None:
            return
        scale = 1.2 if event.button == 'up' else 1 / 1.2
        ax.set_xlim([xdata - (xdata - cur_xlim[0]) * scale,
                     xdata + (cur_xlim[1] - xdata) * scale])
        ax.set_ylim([ydata - (ydata - cur_ylim[0]) * scale,
                     ydata + (cur_ylim[1] - ydata) * scale])
        fig.canvas.draw_idle()

    def on_press(event):
        if event.button != 3:
            return
        global x0, y0
        x0, y0 = event.xdata, event.ydata

    def on_motion(event):
        if event.button != 3 or x0 is None:
            return
        dx = event.xdata - x0
        dy = event.ydata - y0
        ax.set_xlim(ax.get_xlim()[0] - dx, ax.get_xlim()[1] - dx)
        ax.set_ylim(ax.get_ylim()[0] - dy, ax.get_ylim()[1] - dy)
        fig.canvas.draw_idle()

    fig.canvas.mpl_connect('scroll_event', on_scroll)
    fig.canvas.mpl_connect('button_press_event', on_press)
    fig.canvas.mpl_connect('motion_notify_event', on_motion)


def AddNodeInterface(): #Sirve para poder añadir nodos
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

def AddSegmentInterface(): #Sirve para poder añadir segmentos
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


# Función para encontrar el camino más corto
def FindShortestPath():
    global window_graph
    start_name = simpledialog.askstring("Find path", "Origin node:", parent=root)
    end_name = simpledialog.askstring("Find path", "Destination node:", parent=root)
    path = find_shortest_path(window_graph, start_name, end_name)  # Delegamos en path.py

    if not path:
        messagebox.showinfo("Without path", "There is no path between the selected nodes")
        return

    for widget in fig_frame.winfo_children():
        widget.destroy()
    fig, ax = plot.subplots(figsize=(6, 6))
    ax.set_title(f"Shortest path from {start_name} to {end_name}")
    path_node_names = [n.name for n in path]
    for node in window_graph.nodes:
        color = 'blue' if node.name in path_node_names else 'gray'
        ax.scatter(node.x, node.y, color=color, s=100)
        txt=ax.text(node.x, node.y, node.name, fontsize=12, ha='right')
        txt.set_clip_on(True)
    for segment in window_graph.segments:
        if segment.origin in path and segment.destination in path:
            try:
                idx = path.index(segment.origin)
                if path[idx + 1] == segment.destination:
                    color = 'blue'
                    lw = 2
                else:
                    color = 'lightgray'
                    lw = 0.75
            except (ValueError, IndexError):
                color = 'lightgray'
                lw = 0.75
        else:
            color = 'lightgray'
            lw = 0.75
        arrow = FancyArrowPatch((segment.origin.x, segment.origin.y),(segment.destination.x, segment.destination.y), arrowstyle='->', color=color,mutation_scale=15, lw=lw, clip_on=True)
        ax.add_patch(arrow)
    ax.set_aspect('equal',adjustable='box')
    ZoomGraph(fig, ax, fig_frame)



#Pasamos de Airspace a Graph
def AirspacetoGraph(g,a):
    origin = ''
    destination = ''
    for n in a.navpoints:
        AddNode(g, Node(n.name, n.longitude, n.latitude))
    for s in a.navsegments:
        for navPoint in a.navpoints:
            if navPoint.number == s.origin_number:
                origin = navPoint.name
            elif navPoint.number == s.destination_number:
                destination = navPoint.name
        AddSegment(g, origin, destination)



#Mostramos el grafo en función de los ficheros
def ShowAirSpaceGraph1():
    global window_graph
    window_graph = Graph()
    a = CreateGraph4("Cat_nav.txt", "Cat_seg.txt", "Cat_aer.txt")
    AirspacetoGraph(window_graph, a)
    PlotGraph(window_graph)


def ShowAirSpaceGraph2():
    global window_graph
    window_graph = Graph()
    a = CreateGraph4("ECAC_nav.txt","ECAC_seg.txt","ECAC_aer.txt")
    AirspacetoGraph(window_graph, a)
    PlotGraph(window_graph)

def ShowAirSpaceGraph3():
    global window_graph
    window_graph = Graph()
    a = CreateGraph4("Spain_nav.txt","Spain_seg.txt","Spain_aer.txt")
    AirspacetoGraph(window_graph, a)
    PlotGraph(window_graph)


def ActualizeGraphTogger(): #Vuelve a dibujar el gráfico según se cambia la posición del botón
    global window_graph
    PlotGraph(window_graph)


selected_origin = None  # Variable global que guarda el node clickat com a origen

def Click(event): #Sirve para mostrar vecinos y shortest path con clicks del ratón
    global selected_origin, window_graph
    if event.xdata is None or event.ydata is None:
        return
    click_point = (event.xdata, event.ydata)
    threshold = 0.5
    closest_node = None
    min_dist = float('inf')
    for node in window_graph.nodes:
        dist = ((node.x - click_point[0])**2 + (node.y - click_point[1])**2)**0.5
        if dist < min_dist and dist < threshold:
            min_dist = dist
            closest_node = node

    if closest_node is None:
        return

    if event.button == 1:  # Clic izquierdo
        selected_origin = closest_node
        neighbors = closest_node.neighbors

        if neighbors:
            neighbor_names = [n.name for n in neighbors]
            messagebox.showinfo("Neighbors", f"Neighbors of {closest_node.name}: {', '.join(neighbor_names)}")
        else:
            messagebox.showinfo("Neighbors", f"No neighbors found for node {closest_node.name}")

        for widget in fig_frame.winfo_children():
            widget.destroy()

        fig, ax = plot.subplots(figsize=(6, 6))
        ax.set_title(f"Neighbors of {closest_node.name}")

        for node in window_graph.nodes:
            if node == closest_node:
                color = 'blue'
            elif node in neighbors:
                color = 'lightskyblue'
            else:
                color = 'lightgray'
            ax.scatter(node.x, node.y, color=color, s=100)
            ax.text(node.x, node.y, node.name, fontsize=12, ha='right', clip_on=True)

        for segment in window_graph.segments:
            if (segment.origin == closest_node and segment.destination in neighbors) or \
               (segment.destination == closest_node and segment.origin in neighbors):
                seg_color = 'lightskyblue'
                lw = 2
            else:
                seg_color = 'lightgray'
                lw = 1
            arrow = FancyArrowPatch((segment.origin.x, segment.origin.y), (segment.destination.x, segment.destination.y),
                                    arrowstyle='->', color=seg_color, mutation_scale=15, lw=lw, clip_on=True)
            ax.add_patch(arrow)
        ax.set_aspect('equal', adjustable='box')
        ZoomGraph(fig, ax, fig_frame)

    elif event.button == 3:  # Clic derecho
        if selected_origin is None:
            messagebox.showinfo("Info", "Select origin node first with left click.")
            return
        selected_destination = closest_node
        path = find_shortest_path(window_graph, selected_origin.name, selected_destination.name)

        if not path:
            messagebox.showinfo("Without path", "There is no path between the selected nodes")
        else:
            for widget in fig_frame.winfo_children():
                widget.destroy()

            fig, ax = plot.subplots(figsize=(6, 6))
            ax.set_title(f"Shortest path from {selected_origin.name} to {selected_destination.name}")

            path_node_names = [n.name for n in path]
            for node in window_graph.nodes:
                color = 'blue' if node.name in path_node_names else 'gray'
                ax.scatter(node.x, node.y, color=color, s=100)
                ax.text(node.x, node.y, node.name, fontsize=12, ha='right', clip_on=True)

            for segment in window_graph.segments:
                if segment.origin in path and segment.destination in path:
                    try:
                        idx = path.index(segment.origin)
                        if path[idx + 1] == segment.destination:
                            color = 'blue'
                            lw = 2
                        else:
                            color = 'lightgray'
                            lw = 0.75
                    except (ValueError, IndexError):
                        color = 'lightgray'
                        lw = 0.75
                else:
                    color = 'lightgray'
                    lw = 0.75

                arrow = FancyArrowPatch((segment.origin.x, segment.origin.y), (segment.destination.x, segment.destination.y),
                                        arrowstyle='->', color=color, mutation_scale=15, lw=lw, clip_on=True)
                ax.add_patch(arrow)
            ax.set_aspect('equal', adjustable='box')
            ZoomGraph(fig, ax, fig_frame)
        selected_origin = None


def ShowFixedImage(): #Mostra la imatge del grup
    image_path = "grupo.png"

    try:
        img = Image.open(image_path)
        img = img.resize((400, 400), Image.Resampling.LANCZOS)
        img_tk = ImageTk.PhotoImage(img)

        for widget in fig_frame.winfo_children():
            widget.destroy()

        label = tk.Label(fig_frame, image=img_tk)
        label.image = img_tk
        label.pack(expand=True)
    except Exception as e:
        messagebox.showerror("Error", f"Could not load image: {e}")


def ConvertToKML(): #Converteix les coordenades a kml per posar a google earth
    global window_graph
    output_file = filedialog.asksaveasfilename(defaultextension=".kml",filetypes=[("KML Files", "*.kml")],title="Save KML File")

    if not output_file:
        return

    kml = simplekml.Kml()

    for node in window_graph.nodes:
        kml.newpoint(name=node.name,coords=[(node.x, node.y)],description=f"Navigation Point: {node.name}")

    for segment in window_graph.segments:
        line = kml.newlinestring(name=f"{segment.origin.name}-{segment.destination.name}", coords=[(segment.origin.x, segment.origin.y),(segment.destination.x, segment.destination.y)],description=f"Navigation Segment")
        line.style.linestyle.color = simplekml.Color.red
        line.style.linestyle.width = 2

    kml.save(output_file)


def GetAirportWeather(): #Dóna info sobre el weather del aeroport
    airport_code = simpledialog.askstring("Airport Weather", "Enter airport ICAO code",
                                          parent=root)
    if not airport_code:
        return

    try:
        url = f"https://aviationweather.gov/api/data/metar?ids={airport_code}&format=json"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        if not data:
            messagebox.showerror("Error", f"No weather data found for {airport_code}")
            return

        metar = data[0]['rawOb']
        observation_time = data[0]['receiptTime']

        weather_window = tk.Toplevel(root)
        weather_window.title(f"Live Weather for {airport_code}")
        weather_window.geometry("600x400")

        main_frame = ttk.Frame(weather_window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        title_label = ttk.Label(main_frame, text=f"Current meteorology for {airport_code}🛫", font=('Helvetica', 20, 'bold'))
        title_label.pack(pady=(0, 10))

        metar_frame = ttk.LabelFrame(main_frame, text="Raw METAR", padding="10")
        metar_frame.pack(fill=tk.X, pady=5)

        metar_text = tk.Text(metar_frame, height=3, wrap=tk.WORD, font=('Courier', 16), bg='#f0f0f0', padx=5, pady=5)
        metar_text.insert(tk.END, f"{observation_time}\n{metar}")
        metar_text.config(state=tk.DISABLED)
        metar_text.pack(fill=tk.X)

        decode_frame = ttk.LabelFrame(main_frame, text="Decoded Information", padding="10")
        decode_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        decoded_text = tk.Text(decode_frame, wrap=tk.WORD, padx=5, pady=5)

        # Configure text tags for styling
        decoded_text.tag_configure('header', foreground='blue', font=('Helvetica', 20, 'bold'))
        decoded_text.tag_configure('important', foreground='red')
        decoded_text.tag_configure('normal', font=('Helvetica', 18))

        try:

            decoded_text.insert(tk.END, "Observation Time:\n", 'header')
            decoded_text.insert(tk.END, f"{observation_time} (UTC)\n\n", 'normal')

            decoded_text.insert(tk.END, "Wind:\n", 'header')
            if 'KT' in metar:
                wind_part = metar.split('KT')[0].split()[-1] + 'KT'
                wind_dir = wind_part[:3]
                wind_speed = wind_part[3:5]
                decoded_text.insert(tk.END, f"Direction: {wind_dir}°\nSpeed: {wind_speed} knots\n\n", 'normal')

            decoded_text.insert(tk.END, "Visibility:\n", 'header')
            if '9999' in metar:
                decoded_text.insert(tk.END, "10km or more\n\n", 'normal')
            else:
                vis_part = [p for p in metar.split() if 'SM' in p or p.isdigit()][0]
                decoded_text.insert(tk.END, f"{vis_part}\n\n", 'normal')

            decoded_text.insert(tk.END, "Weather Phenomena:\n", 'header')
            wx_codes = {'RA': 'Rain', 'SN': 'Snow', 'TS': 'Thunderstorm', 'FG': 'Fog',
                        'BR': 'Mist', 'HZ': 'Haze', 'DU': 'Dust', 'GR': 'Hail'}
            wx_present = False
            for code, desc in wx_codes.items():
                if code in metar:
                    decoded_text.insert(tk.END, f"{desc} ", 'important')
                    wx_present = True
            if not wx_present:
                decoded_text.insert(tk.END, "No significant weather", 'normal')
            decoded_text.insert(tk.END, "\n\n", 'normal')

            decoded_text.insert(tk.END, "Clouds:\n", 'header')
            cloud_codes = {'FEW': 'Few', 'SCT': 'Scattered', 'BKN': 'Broken', 'OVC': 'Overcast'}
            cloud_info = []
            for part in metar.split():
                if part[:3] in cloud_codes:
                    cloud_info.append(f"{cloud_codes[part[:3]]} at {part[3:]}00 ft")
            if cloud_info:
                decoded_text.insert(tk.END, "\n".join(cloud_info) + "\n\n", 'normal')
            else:
                decoded_text.insert(tk.END, "Clear skies\n\n", 'normal')

            decoded_text.insert(tk.END, "Temperature:\n", 'header')
            if '/' in metar:
                temp_part = [p for p in metar.split() if '/' in p][0]
                temp, dewpoint = temp_part.split('/')
                decoded_text.insert(tk.END, f"Air: {temp}°C\nDew Point: {dewpoint}°C\n\n", 'normal')

            decoded_text.insert(tk.END, "Pressure:\n", 'header')
            if 'Q' in metar:
                q_part = [p for p in metar.split() if p.startswith('Q')][0]
                pressure = q_part[1:]
                decoded_text.insert(tk.END, f"{pressure} hPa\n", 'normal')

        except Exception as e:
            decoded_text.insert(tk.END, f"\nError parsing METAR details: {str(e)}", 'important')

        decoded_text.config(state=tk.DISABLED)
        decoded_text.pack(fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(decode_frame, orient=tk.VERTICAL, command=decoded_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        decoded_text.config(yscrollcommand=scrollbar.set)

    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Failed to fetch weather data: {e}")
    except (KeyError, IndexError):
        messagebox.showerror("Error", "Invalid or unavailable airport code")

def on_tab_change(event):
    selected_tab = event.widget.index("current")

    for widget in fig_frame.winfo_children():
        widget.destroy()

    if selected_tab == 2:
        label = tk.Label(fig_frame, text="EXTRA FUNCTIONALITIES: \n\n\n 1.Buttons to show/hide nodes, segments, SIDs and STARs \n\n 2.Button for the weather of each airport \n\n 3.Try to zoom the graph by using your mouse \n\n 4.Click a node with the left button of the mouse to see it's neighbours \n then click another node with the right button of your mouse to see \n the shortest path between both nodes", font=("Arial", 14))
        label.pack(expand=True)











# Interfaz gráfica
window_graph = Graph()
root = tk.Tk()
show_distance=tk.BooleanVar(value=False)
show_nodes=tk.BooleanVar(value=True)
show_sids = tk.BooleanVar(value=True)
show_stars = tk.BooleanVar(value=True)
root.title("Graph viewer")
root.geometry("1000x600")

# Crear un frame para los botones
left_panel = ttk.Frame(root, width=250)  # Frame de botones, especificamos un tamaño fijo
left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)  # Coloca los botones a la izquierda

#Creamos pestañas utilizando Notebook
tabla_control = ttk.Notebook(left_panel)
tabla_control.bind("<<NotebookTabChanged>>", on_tab_change)
pestanya1 = ttk.Frame(tabla_control)
pestanya2 = ttk.Frame(tabla_control)
pestanya3 = ttk.Frame(tabla_control)
pestanya4 = ttk.Frame(tabla_control)
tabla_control.add(pestanya1, text="Graphs")
tabla_control.add(pestanya2, text="Airspace")
tabla_control.add(pestanya3, text="Extra functionalities")
tabla_control.add(pestanya4, text="Team")
tabla_control.bind("<<NotebookTabChanged>>", on_tab_change)


#Mostrar el notebook (pestañas)
tabla_control.pack(expand=True,fill='both')

# Crear un frame para el gráfico
fig_frame = ttk.Frame(root)
fig_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)  # Coloca el gráfico a la derecha

# Botones de la interfaz (en el frame de botones)
show_example_button = ttk.Button(pestanya1, text="Show example graph", command=ShowExampleGraph)
show_example_button.pack(pady=10)

show_custom_button = ttk.Button(pestanya1, text="Show invented graph", command=ShowCustomGraph)
show_custom_button.pack(pady=10)

load_file_button = ttk.Button(pestanya1, text="Load graph from file", command=LoadGraph)
load_file_button.pack(pady=10)

airspace_button1 = ttk.Button(pestanya2, text="Catalunya Airspace", command=ShowAirSpaceGraph1)
airspace_button1.pack(pady=10)

airspace_button2=ttk.Button(pestanya2,text="Europe Airspace",command=ShowAirSpaceGraph2)
airspace_button2.pack(pady=10)

airspace_button3=ttk.Button(pestanya2,text="Spain Airspace",command=ShowAirSpaceGraph3)
airspace_button3.pack(pady=10)

add_node_button = ttk.Button(pestanya1, text="Add node", command=AddNodeInterface)
add_node_button.pack(pady=10)

add_node_button = ttk.Button(pestanya2, text="Add node", command=AddNodeInterface)
add_node_button.pack(pady=10)

add_segment_button = ttk.Button(pestanya1, text="Add segment", command=AddSegmentInterface)
add_segment_button.pack(pady=10)

add_segment_button = ttk.Button(pestanya2, text="Add segment", command=AddSegmentInterface)
add_segment_button.pack(pady=10)

select_node_button = ttk.Button(pestanya1, text="Select nodes for neighbours", command=SelectNode)
select_node_button.pack(pady=10)

select_node_button = ttk.Button(pestanya2, text="Select nodes for neighbours", command=SelectNode)
select_node_button.pack(pady=10)

find_path_button = ttk.Button(pestanya1, text="Shortest path between nodes", command=FindShortestPath)
find_path_button.pack(pady=10)

find_path_button = ttk.Button(pestanya2, text="Shortest path between nodes", command=FindShortestPath)
find_path_button.pack(pady=10)

show_distance_button = ttk.Checkbutton(pestanya1,text="Show distance between nodes",variable=show_distance,command=ActualizeGraphTogger)
show_distance_button.pack(pady=10)

show_nodes_button=ttk.Checkbutton(pestanya1,text="Show nodes name",variable=show_nodes,command=ActualizeGraphTogger)
show_nodes_button.pack(pady=10)

weather_button = ttk.Button(pestanya2, text="Get Airport Weather⛅️", command=GetAirportWeather)
weather_button.pack(pady=10)

show_distance_button = ttk.Checkbutton(pestanya2,text="Show distance between nodes",variable=show_distance,command=ActualizeGraphTogger)
show_distance_button.pack(pady=10)

show_nodes_button=ttk.Checkbutton(pestanya2,text="Show nodes name",variable=show_nodes,command=ActualizeGraphTogger)
show_nodes_button.pack(pady=10)

show_sids_button=ttk.Checkbutton(pestanya2,text="Show SIDs",variable=show_sids,command=lambda:PlotGraph(window_graph))
show_sids_button.pack(pady=10)

show_stars_button=ttk.Checkbutton(pestanya2,text="Show STARs",variable=show_stars,command=lambda:PlotGraph(window_graph))
show_stars_button.pack(pady=10)

show_team_image_button = ttk.Button(pestanya4, text="Show team photo", command=ShowFixedImage)
show_team_image_button.pack(pady=10)

kml_button = ttk.Button(pestanya1, text="Save KML", command=ConvertToKML)
kml_button.pack(pady=10)

kml_button = ttk.Button(pestanya2, text="Save KML️", command=ConvertToKML)
kml_button.pack(pady=10)

#We already converted to KML once so we erased the buttons to do it again




root.mainloop()
