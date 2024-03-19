import tkinter as tk
from tkinter import messagebox

class GraphDrawerApp:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=800, height=600, bg="white")
        self.canvas.pack(expand=True, fill="both")
        self.canvas.bind("<Button-1>", self.create_node)
        self.canvas.bind("<Button-3>", self.create_edge)  # Botón derecho del mouse para crear aristas
        self.canvas.bind("<Control-Button-1>", self.create_edge_ctrl)  # Ctrl + clic izquierdo para crear aristas
        self.nodes = []
        self.edges = []
        self.selected_node = None
        self.highlighted_nodes = []

    def create_node(self, event):
        x, y = event.x, event.y
        node = self.canvas.create_oval(x-10, y-10, x+10, y+10, fill="blue")
        self.nodes.append((node, x, y))  # Guardar el nodo con sus coordenadas

    def create_edge(self, event):
        # Esta función se ejecuta cuando se hace clic derecho
        if self.selected_node is not None:
            # Obtener las coordenadas del nodo sobre el cual se hizo clic
            x, y = event.x, event.y
            # Crear la arista
            edge = self.canvas.create_line(self.nodes[self.selected_node][1], self.nodes[self.selected_node][2], x, y, fill="black")
            self.edges.append((self.selected_node, len(self.nodes) - 1))
            # Restaurar el color de los nodos destacados
            self.restore_highlighted_nodes()
            # Reiniciar el nodo seleccionado
            self.selected_node = None

    def create_edge_ctrl(self, event):
        # Esta función se ejecuta cuando se mantiene presionada la tecla Ctrl y se hace clic izquierdo
        for i, (node, node_x, node_y) in enumerate(self.nodes):
            # Comprobar si el clic ocurrió dentro de un nodo
            if abs(event.x - node_x) <= 10 and abs(event.y - node_y) <= 10:
                if self.selected_node is None:
                    # Cambiar el color del nodo seleccionado a azul claro
                    self.canvas.itemconfig(node, fill="lightblue")
                    self.highlighted_nodes.append(node)
                    self.selected_node = i
                    break
                else:
                    if self.selected_node != i:
                        # Crear la arista
                        edge = self.canvas.create_line(self.nodes[self.selected_node][1], self.nodes[self.selected_node][2], node_x, node_y, fill="black")
                        self.edges.append((self.selected_node, i))
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
        for node in self.highlighted_nodes:
            self.canvas.itemconfig(node, fill="blue")
        self.highlighted_nodes = []

    def show_graph_info(self):
        messagebox.showinfo("Información del Grafo", f"Número de nodos: {len(self.nodes)}\nNúmero de aristas: {len(self.edges)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = GraphDrawerApp(root)
    button = tk.Button(root, text="Mostrar Información del Grafo", command=app.show_graph_info)
    button.pack()
    root.mainloop()