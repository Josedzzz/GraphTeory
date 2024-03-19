import tkinter as tk
from tkinter import messagebox, simpledialog
import networkx as nx

class GraphDrawerApp:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=800, height=600, bg="white")
        self.canvas.pack(expand=True, fill="both")
        self.canvas.bind("<Button-1>", self.create_node)
        self.canvas.bind("<Button-3>", self.create_edge)  # Botón derecho del mouse para crear aristas
        self.canvas.bind("<Control-Button-1>", self.create_edge_ctrl)  # Ctrl + clic izquierdo para crear aristas
        self.nodes = {}  # Utilizaremos un diccionario para almacenar los nodos con sus nombres como clave
        self.edges = []
        self.selected_node = None
        self.highlighted_nodes = []
        self.graph = nx.Graph()

    def create_node(self, event):
        # Pedir al usuario el nombre del nodo
        node_name = simpledialog.askstring("Nombre del nodo", "Ingrese el nombre del nodo:")
        if node_name is not None:
            if node_name not in self.nodes:  # Verificar que el nombre no se repita
                x, y = event.x, event.y
                node = self.canvas.create_oval(x-10, y-10, x+10, y+10, fill="blue")
                self.nodes[node_name] = (node, x, y)  # Guardar el nodo con su nombre y coordenadas
                self.graph.add_node(node_name)
                # Mostrar el nombre del nodo junto al nodo
                self.canvas.create_text(x, y, text=node_name, fill="black", anchor="center")
            else:
                messagebox.showwarning("Nombre duplicado", f"El nombre '{node_name}' ya está en uso. Por favor, ingrese un nombre diferente.")

    def create_edge(self, event):
        # Esta función se ejecuta cuando se hace clic derecho
        if self.selected_node is not None:
            # Obtener las coordenadas del nodo sobre el cual se hizo clic
            x, y = event.x, event.y
            # Crear la arista
            edge = self.canvas.create_line(self.nodes[self.selected_node][1], self.nodes[self.selected_node][2], x, y, fill="black")
            self.edges.append((self.selected_node, len(self.nodes) - 1))
            self.graph.add_edge(self.selected_node, list(self.nodes.keys())[-1])  # El último nodo creado
            # Restaurar el color de los nodos destacados
            self.restore_highlighted_nodes()
            # Reiniciar el nodo seleccionado
            self.selected_node = None

    def create_edge_ctrl(self, event):
        # Esta función se ejecuta cuando se mantiene presionada la tecla Ctrl y se hace clic izquierdo
        for node_name, (node, node_x, node_y) in self.nodes.items():
            # Comprobar si el clic ocurrió dentro de un nodo
            if abs(event.x - node_x) <= 10 and abs(event.y - node_y) <= 10:
                if self.selected_node is None:
                    # Cambiar el color del nodo seleccionado a azul claro
                    self.canvas.itemconfig(node, fill="lightblue")
                    self.highlighted_nodes.append(node)
                    self.selected_node = node_name
                    break
                else:
                    if self.selected_node != node_name:
                        # Crear la arista
                        edge = self.canvas.create_line(self.nodes[self.selected_node][1], self.nodes[self.selected_node][2], node_x, node_y, fill="black")
                        self.edges.append((self.selected_node, node_name))
                        self.graph.add_edge(self.selected_node, node_name)
                        # Restaurar el color de los nodos destacados
                        self.restore_highlighted_nodes()
                        # Reiniciar el nodo seleccionado
                        self.selected_node = None
                        break
        else:
            if self.selected_node is not None:
                # Restaurar el color del nodo seleccionado a azul original
                self.canvas.itemconfig(self.nodes[self.selected_node][0], fill="blue")
                self.selected_node = None

    def restore_highlighted_nodes(self):
        # Restaurar el color de los nodos destacados a azul original
        for node, _, _ in self.nodes.values():
            self.canvas.itemconfig(node, fill="blue")
        self.highlighted_nodes = []

    def show_graph_info(self):
        messagebox.showinfo("Información del Grafo", f"Número de nodos: {len(self.nodes)}\nNúmero de aristas: {len(self.edges)}")

    def shortest_path(self, start_node, end_node):
        return nx.shortest_path(self.graph, start_node, end_node)

    def show_shortest_path(self):
        start_node = simpledialog.askstring("Nodo de inicio", "Ingrese el nombre del nodo de inicio:")
        end_node = simpledialog.askstring("Nodo de fin", "Ingrese el nombre del nodo de fin:")
        shortest_path = self.shortest_path(start_node, end_node)
        messagebox.showinfo("Camino más corto", f"El camino más corto entre los nodos {start_node} y {end_node} es: {shortest_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = GraphDrawerApp(root)
    button_info = tk.Button(root, text="Mostrar Información del Grafo", command=app.show_graph_info)
    button_info.pack()
    button_shortest_path = tk.Button(root, text="Camino más corto", command=app.show_shortest_path)
    button_shortest_path.pack()
    root.mainloop()