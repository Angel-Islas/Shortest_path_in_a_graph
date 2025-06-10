import tkinter as tk
from tkinter import filedialog, messagebox
import heapq
import ast
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def cargar_grafo(nombre_archivo):
    try:
        with open(nombre_archivo, 'r') as file:
            info = file.read()
            graph = ast.literal_eval(info)
            return graph
    except Exception as e:
        messagebox.showerror("Error", f"Error al cargar el archivo: {str(e)}")
        return None

def shortest_path(graph, start, end):
    distancia = {node: float('infinity') for node in graph}
    distancia[start] = 0
    previous_nodes = {node: None for node in graph}
    cola_prioridad = [(0, start)]

    while cola_prioridad:
        distancia_actual, nodo_actual = heapq.heappop(cola_prioridad)

        if distancia_actual > distancia[nodo_actual]:
            continue

        for neighbor, weight in graph[nodo_actual]['connections']:
            distance = distancia_actual + weight

            if distance < distancia[neighbor]:
                distancia[neighbor] = distance
                previous_nodes[neighbor] = nodo_actual
                heapq.heappush(cola_prioridad, (distance, neighbor))

    total = distancia[end]
    shortest_path = []
    current = end
    while current is not None:
        shortest_path.insert(0, current)
        current = previous_nodes[current]

    return total, shortest_path

def imprimir_grafo(graph, ax, canvas, shortest_path=None):
    G = nx.Graph()

    for node, data in graph.items():
        G.add_node(node, pos=data['pos'], label=node)
        for neighbor, weight in data['connections']:
            G.add_edge(node, neighbor, weight=weight)

    pos = nx.get_node_attributes(G, 'pos')
    labels = nx.get_node_attributes(G, 'label')
    edge_labels = nx.get_edge_attributes(G, 'weight')

    ax.clear()
    nx.draw(G, pos, with_labels=True, labels=labels, ax=ax, node_size=700, node_color='palegreen', font_weight='bold', font_color='black')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='lightcoral', ax=ax)

    if shortest_path:
        path_edges = [(shortest_path[i], shortest_path[i + 1]) for i in range(len(shortest_path) - 1)]
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='sandybrown', width=2.0, ax=ax)

    canvas.draw()

def abrir_archivo():
    file_path = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
    if file_path:
        grafo = cargar_grafo(file_path)
        if grafo:
            global grafo_final
            grafo_final = grafo
            imprimir_grafo(grafo_final, ax1, canvas1)

def calcular_ruta():
    if not grafo_final:
        messagebox.showwarning("Advertencia", "Primero debes cargar un grafo.")
        return
    
    inicio = entry_inicio.get()
    final = entry_final.get()

    if inicio in grafo_final and final in grafo_final:
        try:
            distance, path = shortest_path(grafo_final, inicio, final)
            messagebox.showinfo("Resultado", f"Distancia más corta: {distance}\nCamino: {path}")

            # Crear una nueva figura y canvas para asegurar que se redibuje correctamente
            global fig2, ax2, canvas2
            fig2, ax2 = plt.subplots(figsize=(5, 5))
            canvas2.get_tk_widget().destroy()  # Destruir el canvas anterior
            canvas2 = FigureCanvasTkAgg(fig2, master=frame3)
            canvas2.get_tk_widget().pack()

            # Dibujar el grafo con el camino resaltado
            imprimir_grafo(grafo_final, ax2, canvas2, shortest_path=path)
        except Exception as e:
            messagebox.showerror("Error", str(e))
    else:
        messagebox.showwarning("Advertencia", "Vertices no válidos.")

# Interfaz gráfica con Tkinter
root = tk.Tk()
root.title("Visualización de Grafos y Camino más Corto")

# Dividir la ventana en tres columnas
frame1 = tk.Frame(root)
frame1.grid(row=0, column=0, padx=10, pady=10)

frame2 = tk.Frame(root)
frame2.grid(row=0, column=1, padx=10, pady=10)

frame3 = tk.Frame(root)
frame3.grid(row=0, column=2, padx=10, pady=10)

# Columna 1 (Cargar archivo y seleccionar nodos)
btn_abrir = tk.Button(frame1, text="Cargar Archivo", command=abrir_archivo)
btn_abrir.pack(pady=5)

label_inicio = tk.Label(frame1, text="Nodo de Inicio:")
label_inicio.pack()

entry_inicio = tk.Entry(frame1)
entry_inicio.pack(pady=5)

label_final = tk.Label(frame1, text="Nodo de Destino:")
label_final.pack()

entry_final = tk.Entry(frame1)
entry_final.pack(pady=5)

btn_calcular = tk.Button(frame1, text="Calcular Camino", command=calcular_ruta)
btn_calcular.pack(pady=10)

# Columna 2 (Visualización del grafo original)
fig1, ax1 = plt.subplots(figsize=(5, 5))
canvas1 = FigureCanvasTkAgg(fig1, master=frame2)
canvas1.get_tk_widget().pack()

# Columna 3 (Visualización del grafo con camino resaltado)
fig2, ax2 = plt.subplots(figsize=(5, 5))
canvas2 = FigureCanvasTkAgg(fig2, master=frame3)
canvas2.get_tk_widget().pack()

# Variable global para el grafo
grafo_final = None

root.mainloop()
