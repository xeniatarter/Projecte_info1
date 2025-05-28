import tkinter as tk
from PIL import Image, ImageTk
import requests
import io
import subprocess
import sys
import os

# Crear ventana
splash = tk.Tk()
splash.title("Graph Viewer")
splash.attributes('-fullscreen', True)  # Ocupa toda la pantalla

# Obtener tamaño de pantalla
screen_width = splash.winfo_screenwidth()
screen_height = splash.winfo_screenheight()

# Descargar la imagen y redimensionarla al tamaño de la pantalla
url = "https://assetsio.gnwcdn.com/microsoft-flight-simulator.jpg?width=1600&height=900&fit=crop&quality=100&format=png&enable=upscale&auto=webp"
response = requests.get(url)
image_data = response.content
image = Image.open(io.BytesIO(image_data))
image = image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
photo = ImageTk.PhotoImage(image)

# Imagen como fondo
background_label = tk.Label(splash, image=photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Función para abrir el otro script
def open_interface():
    splash.destroy()
    script_path = os.path.join(os.path.dirname(__file__), 'interface.py')
    subprocess.Popen([sys.executable, script_path])

# Botón centrado en la parte inferior
start_button = tk.Button(splash, text="Get Started", font=("Helvetica", 16, "bold"),
                         bg="#FFD700", fg="#000", command=open_interface)
start_button.place(relx=0.5, rely=0.9, anchor="center")  # 90% hacia abajo

splash.mainloop()
