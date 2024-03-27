import tkinter as tk
from tkinter import messagebox, simpledialog
import networkx as nx

class GraphDrawerApp:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=800, height=500, bg="white")
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
                node = self.canvas.create_oval(x-10, y-10, x+10, y+10, fill="#14D0E8")
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
                self.canvas.itemconfig(self.nodes[self.selected_node][0], fill="#14D0E8")
                self.selected_node = None

    def restore_highlighted_nodes(self):
        # Restaurar el color de los nodos destacados a azul original
        for node, _, _ in self.nodes.values():
            self.canvas.itemconfig(node, fill="#14D0E8")
        self.highlighted_nodes = []


    #FUNCIONES CON LAS QUE INTERACTUA EL USUARIO --------------------------------------------------------------------------------

    def show_graph_info(self):
        messagebox.showinfo("Información del Grafo", f"Número de nodos: {len(self.nodes)}\nNúmero de aristas: {len(self.edges)}")

    # Muestra los nodos del grafo denotando correctamnete
    def show_graph_nodes(self):
        if self.nodes:
            node_list = ", ".join(self.nodes.keys())
            messagebox.showinfo("Nodos del Grafo", f"V(G) = {{{node_list}}}")
        else:
            messagebox.showinfo("Nodos del Grafo", "El grafo no tiene nodos.")

    # Muestra las aristas del grafo denotando correctamente
    def show_graph_edges(self):
        if self.edges:
            edge_list = ", ".join([f"({edge[0]}, {edge[1]})" for edge in self.edges])
            messagebox.showinfo("Aristas del Grafo", f"E(G) = {{{edge_list}}}")
        else:
            messagebox.showinfo("Aristas del Grafo", "El grafo no tiene aristas.")

    def show_neighbors(self):
        # Pedir al usuario el nombre del vértice
        vertex_name = simpledialog.askstring("Vértice", "Ingrese el nombre del vértice para ver sus vecinos:")
        if vertex_name is not None:
            if vertex_name in self.nodes:
                neighbors = list(self.graph.neighbors(vertex_name))
                if neighbors:
                    messagebox.showinfo("Vecinos", f"Los vecinos de {vertex_name} son: {', '.join(neighbors)}")
                else:
                    messagebox.showinfo("Vecinos", f"{vertex_name} no tiene vecinos.")
            else:
                messagebox.showwarning("Vértice no encontrado", f"No se encontró el vértice {vertex_name} en el grafo.")    


    def shortest_path(self, start_node, end_node):
        return nx.shortest_path(self.graph, start_node, end_node)

    def show_shortest_path(self):
        start_node = simpledialog.askstring("Nodo de inicio", "Ingrese el nombre del nodo de inicio:")
        end_node = simpledialog.askstring("Nodo de fin", "Ingrese el nombre del nodo de fin:")
        shortest_path = self.shortest_path(start_node, end_node)
        messagebox.showinfo("Camino más corto", f"El camino más corto entre los nodos {start_node} y {end_node} es: {shortest_path}")

    # Función para verificar si el grafo tiene un camino de Euler
    def eulerian_path(self):
        odd_degree_nodes = [node for node, deg in self.graph.degree() if deg % 2 == 1]
        if len(odd_degree_nodes) != 0 and len(odd_degree_nodes) != 2:
            return False, None  # No hay camino de Euler

        temp_graph = self.graph.copy()
        euler_path = []
        current_node = odd_degree_nodes[0] if odd_degree_nodes else next(iter(temp_graph.nodes))

        while temp_graph.edges:
            for neighbor in nx.neighbors(temp_graph, current_node):
                temp_graph.remove_edge(current_node, neighbor)
                if not nx.is_connected(temp_graph.subgraph(nx.node_connected_component(temp_graph, current_node))):
                    temp_graph.add_edge(current_node, neighbor)
                    continue
                euler_path.append((current_node, neighbor))
                current_node = neighbor
                break

        if len(euler_path) == self.graph.number_of_edges():
            return True, euler_path
        else:
            return False, None  # No hay camino de Euler


    # Función para mostrar el camino de Euler si existe
    def show_eulerian_path(self):
        is_eulerian, euler_path = self.eulerian_path()
        if is_eulerian:
            path_str = ' -> '.join(f"{edge[0]}-{edge[1]}" for edge in euler_path)
            messagebox.showinfo("Camino de Euler", f"El grafo tiene un camino de Euler:\n{path_str}")
        else:
            messagebox.showinfo("Camino de Euler", "El grafo no tiene un camino de Euler.")

    # Funcion para limpiar el lienzo
    def clear_canvas(self):
        # Limpia el lienzo
        self.canvas.delete("all")
        self.nodes = {}
        self.edges = []
        self.graph.clear()

    # Funcion para borrar un nodo seleccionado
    def delete_selected_node(self):
        if self.selected_node is not None:
            # Eliminar el nodo seleccionado y sus aristas
            self.canvas.delete(self.nodes[self.selected_node][0])  # Eliminar la representación visual del nodo
            del self.nodes[self.selected_node]  # Eliminar el nodo del diccionario de nodos
            self.graph.remove_node(self.selected_node)  # Eliminar el nodo del grafo
            self.edges = [(n1, n2) for n1, n2 in self.edges if n1 != self.selected_node and n2 != self.selected_node]  # Eliminar las aristas conectadas al nodo seleccionado
            self.selected_node = None
            # Actualizar el lienzo
            self.update_canvas()


    # Actualiza el lienzo
    def update_canvas(self):
        # Limpiar el lienzo
        self.canvas.delete("all")
        # Dibujar nodos
        for node_name, (node, x, y) in self.nodes.items():
            self.canvas.create_oval(x-10, y-10, x+10, y+10, fill="#14D0E8")
            self.canvas.create_text(x, y, text=node_name, fill="black", anchor="center")
        # Dibujar aristas
        for edge in self.edges:
            node1, node2 = edge
            x1, y1 = self.nodes[node1][1], self.nodes[node1][2]
            x2, y2 = self.nodes[node2][1], self.nodes[node2][2]
            self.canvas.create_line(x1, y1, x2, y2, fill="black")

if __name__ == "__main__":
    root = tk.Tk()
    app = GraphDrawerApp(root)
    root.attributes('-zoomed', True)

    button_frame = tk.Frame(root)  # Crear un Frame para los botones
    button_frame.pack(side=tk.BOTTOM, fill=tk.X)  # Colocar el Frame en la parte inferior y que ocupe todo el ancho
    
    button_info = tk.Button(button_frame, text="Mostrar Información del Grafo", command=app.show_graph_info)
    button_info.pack(side=tk.LEFT, padx=5, pady=5)  # Acomodar el botón a la izquierda con un poco de espacio
    
    button_nodes = tk.Button(button_frame, text="Mostrar Nodos", command=app.show_graph_nodes)
    button_nodes.pack(side=tk.LEFT, padx=5, pady=5)  # Acomodar el botón a la izquierda con un poco de espacio
    
    button_edges = tk.Button(button_frame, text="Mostrar Aristas", command=app.show_graph_edges)
    button_edges.pack(side=tk.LEFT, padx=5, pady=5)  # Acomodar el botón a la izquierda con un poco de espacio
    
    button_shortest_path = tk.Button(button_frame, text="Camino más corto", command=app.show_shortest_path)
    button_shortest_path.pack(side=tk.LEFT, padx=5, pady=5)  # Acomodar el botón a la izquierda con un poco de espacio
    
    button_eulerian_path = tk.Button(button_frame, text="Camino de Euler", command=app.show_eulerian_path)
    button_eulerian_path.pack(side=tk.LEFT, padx=5, pady=5)  # Acomodar el botón a la izquierda con un poco de espacio

    button_show_neighbors = tk.Button(button_frame, text="Mostrar Vecinos", command=app.show_neighbors)
    button_show_neighbors.pack(side=tk.LEFT, padx=5, pady=5)  # Acomodar el botón a la izquierda con un poco de espacio
    
    # Botón para limpiar el lienzo
    clear_button = tk.Button(button_frame, text="Limpiar", command=app.clear_canvas)
    clear_button.pack(side=tk.LEFT, padx=5, pady=5)  # Acomodar el botón a la derecha con un poco de espacio
    
    # Botón para eliminar un nodo
    delete_button = tk.Button(button_frame, text="Eliminar Nodo", command=app.delete_selected_node)
    delete_button.pack(side=tk.LEFT, padx=5, pady=5)  # Acomodar el botón a la derecha con un poco de espacio
    
    root.mainloop()
    