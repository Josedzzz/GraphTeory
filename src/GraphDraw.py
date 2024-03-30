import tkinter as tk
from tkinter import messagebox, simpledialog
import networkx as nx
import numpy as np


class GraphDrawerApp:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=800, height=500, bg="white")
        self.canvas.pack(expand=True, fill="both")
        self.canvas.bind("<Button-1>", self.create_node)
        self.canvas.bind("<Control-Button-1>", self.create_edge_ctrl)  # Ctrl + clic izquierdo para crear aristas
        self.nodes = {}  # Utilizaremos un diccionario para almacenar los nodos con sus nombres como clave
        self.edges = []
        self.selected_node = None
        self.highlighted_nodes = []
        self.graph = nx.Graph()
        self.graph_edges = {}  # Diccionario para mapear pares de nodos a las aristas dibujadas


    # Crea graficamente un nodo
    def create_node(self, event):
        node_name = simpledialog.askstring("Nombre del nodo", "Ingrese el nombre del nodo:")
        if node_name is not None:
            if node_name not in self.nodes:  
                x, y = event.x, event.y
                node = self.canvas.create_oval(x-10, y-10, x+10, y+10, fill="#14D0E8")
                self.nodes[node_name] = (node, x, y)  # Guardar el nodo con su nombre y coordenadas
                self.graph.add_node(node_name)
                # Mostrar el nombre del nodo junto al nodo
                self.canvas.create_text(x, y, text=node_name, fill="black", anchor="center")
            else:
                messagebox.showwarning("Nombre duplicado", f"El nombre '{node_name}' ya está en uso. Por favor, ingrese un nombre diferente.")


    # Crea graficamente una arista
    def create_edge_ctrl(self, event):
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
                        self.graph_edges[(self.selected_node, node_name)] = edge  # Agregar la arista al diccionario
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


    # Restaurar el color de los nodos destacados a azul original
    def restore_highlighted_nodes(self):
        for node, _, _ in self.nodes.values():
            self.canvas.itemconfig(node, fill="#14D0E8")
        self.highlighted_nodes = []


    #FUNCIONES CON LAS QUE INTERACTUA EL USUARIO --------------------------------------------------------------------------------

    # Muestra informacion basica del grafo
    def show_graph_info(self):
        info_message = f"Número de nodos: {len(self.nodes)}\nNúmero de aristas: {len(self.edges)}\n"

        if self.is_simple_graph():
            info_message += "El grafo es un grafo simple\n"
        elif self.is_multigraph():
            info_message += "El grafo es un multigrafo\n"

        if self.is_regular_graph():
            info_message += "El grafo es regular\n"
        else:
            info_message += "El grafo no es regular\n"

        if self.is_trivial_graph():
            info_message += "El grafo es trivial\n"
        else:
            info_message += "El grafo no es trivial\n"

        messagebox.showinfo("Información del Grafo", info_message)


    # Retorna el valor booleano de si el grafo es simple o no
    def is_simple_graph(self):
        return len(self.edges) == len(set(self.edges))

    # Retorna el valor booleano de si el grafo es un multigrafo o no
    def is_multigraph(self):
        return len(self.edges) != len(set(self.edges))

    # Retorna el valor booleano de si el grafo es uno regular o no
    def is_regular_graph(self):
        if len(self.nodes) == 0:
            return False
        degree_set = set(self.graph.degree(node) for node in self.graph.nodes)
        return len(degree_set) == 1

    # Retorna el valor booleano de si el grafo es trivial o no
    def is_trivial_graph(self):
        return len(self.nodes) == 1


    # Muestra los nodos del grafo 
    def show_graph_nodes(self):
        if self.nodes:
            node_list = ", ".join(self.nodes.keys())
            messagebox.showinfo("Nodos del Grafo", f"V(G) = {{{node_list}}}")
        else:
            messagebox.showinfo("Nodos del Grafo", "El grafo no tiene nodos.")


    # Muestra las aristas del grafo 
    def show_graph_edges(self):
        if self.edges:
            edge_list = ", ".join([f"({edge[0]}, {edge[1]})" for edge in self.edges])
            messagebox.showinfo("Aristas del Grafo", f"E(G) = {{{edge_list}}}")
        else:
            messagebox.showinfo("Aristas del Grafo", "El grafo no tiene aristas.")


    # Muestra los vecinos de un nodo        
    def show_node_neighbors(self):
        # Pedir al usuario el nombre del nodo
        node_name = simpledialog.askstring("Vecinos del Nodo", "Ingrese el nombre del nodo para ver sus vecinos:")
        if node_name is not None:
            if node_name in self.nodes:
                neighbors = list(self.graph.neighbors(node_name))
                if neighbors:
                    neighbors_str = ", ".join(neighbors)
                    messagebox.showinfo("Vecinos", f"n({node_name}) = {{{neighbors_str}}}")
                else:
                    messagebox.showinfo("Vecinos", f"{node_name} no tiene vecinos.")
            else:
                messagebox.showwarning("Nodo no encontrado", f"No se encontró el nodo {node_name} en el grafo.")


    # Muestra el grado de un nodo
    def show_node_degree(self):
        # Pedir al usuario el nombre del nodo
        node_name = simpledialog.askstring("Grado del Nodo", "Ingrese el nombre del nodo para ver su grado:")
        if node_name is not None:
            if node_name in self.nodes:
                degree = self.graph.degree[node_name]
                messagebox.showinfo("Grado del Nodo", f"d({node_name}) = {degree}")
            else:
                messagebox.showwarning("Nodo no encontrado", f"No se encontró el nodo {node_name} en el grafo.")


    # Calcula la matriz de adyacencia
    def calculate_adjacency_matrix(self, power):
        adjacency_matrix = nx.adjacency_matrix(self.graph).todense()
        node_names = list(self.graph.nodes())
        adjacency_matrix_power = np.linalg.matrix_power(adjacency_matrix, power)
        return node_names, adjacency_matrix_power.tolist()


    # Muestra la matriz de adyacencia
    def show_adjacency_matrix(self):
        if self.nodes:  # Verificar si hay nodos en el grafo
            power = simpledialog.askinteger("Potencia", "Ingrese la potencia para calcular la matriz de adyacencia a la k:")
            if power is not None:
                node_names, adjacency_matrix = self.calculate_adjacency_matrix(power)
                # Calcular la longitud máxima de los nombres de columna
                max_name_length = max(len(name) for name in node_names)
                
                # Construir la cadena de la matriz de adyacencia
                matrix_str = " " * (max_name_length + 2)  # Espacio para alinear correctamente las filas
                for name in node_names:
                    matrix_str += name.ljust(max_name_length) + " "
                matrix_str += "\n"
                
                for i, row in enumerate(adjacency_matrix):
                    matrix_str += node_names[i].ljust(max_name_length) + " "  # Alinear correctamente las filas
                    for cell in row:
                        matrix_str += str(cell).ljust(max_name_length) + " "
                    matrix_str += "\n"
                
                messagebox.showinfo("Matriz de Adyacencia", f"Matriz de Adyacencia a la {power}:\n{matrix_str}")
        else:
            messagebox.showwarning("Grafo Vacío", "No hay nodos en el grafo. Cree nodos antes de calcular la matriz de adyacencia.")


    # Calcula la matriz de incidencia
    def calculate_incidence_matrix(self):
        # Crear una lista de nodos y una lista de aristas
        node_list = list(self.nodes.keys())
        edge_list = self.edges

        # Asignar nombres personalizados a las aristas
        edge_names = [f"{n1}-{n2}" for n1, n2 in edge_list]

        # Inicializar la matriz de incidencia con ceros
        incidence_matrix = np.zeros((len(node_list), len(edge_list)), dtype=int)

        # Llenar la matriz de incidencia con los valores correctos
        for i, node in enumerate(node_list):
            for j, (n1, n2) in enumerate(edge_list):
                if node in (n1, n2):
                    incidence_matrix[i, j] = 1

        return incidence_matrix, node_list, edge_names
    

    # Imprime la matriz de incidencia
    def show_incidence_matrix(self):
        incidence_matrix, node_list, edge_names = self.calculate_incidence_matrix()

        # Calculamos el ancho máximo de los nombres de las aristas
        max_edge_name_length = max(len(edge_name) for edge_name in edge_names)

        # Creamos una cadena para las columnas de la matriz
        column_header = "Node".ljust(10)  # Ancho fijo para el nombre del nodo
        for edge_name in edge_names:
            column_header += edge_name.ljust(max_edge_name_length + 5)  # Ancho máximo + 5 espacios de separación
        column_header += "\n"  # Nueva linea despues de los nombres de las aristas

        # Creamos la cadena para el contenido de la matriz
        matrix_str = column_header
        for i, node in enumerate(node_list):
            matrix_str += f"{node}: ".ljust(10)  # Ancho fijo para el nombre del nodo
            for j in range(len(edge_names)):
                matrix_str += f"{incidence_matrix[i, j]}".ljust(max_edge_name_length + 5)  # Ancho máximo + 5 espacios de separación
            matrix_str += "\n"  # Nueva línea después de cada fila

        messagebox.showinfo("Matriz de Incidencia", matrix_str)


    # Retorna el camnino mas corto entre dos nodos
    def shortest_path(self, start_node, end_node):
        return nx.shortest_path(self.graph, start_node, end_node)


    # Muestra el camino mas corto entre los nodos
    def show_shortest_path(self):
        start_node = simpledialog.askstring("Nodo de inicio", "Ingrese el nombre del nodo de inicio:")
        end_node = simpledialog.askstring("Nodo de fin", "Ingrese el nombre del nodo de fin:")
        shortest_path_nodes = self.shortest_path(start_node, end_node)
        
        if shortest_path_nodes:
            # Pintar las aristas del camino mas corto de rojo
            self.highlight_shortest_path(shortest_path_nodes)
            
            # Mostrar el messagebox con el camino mas corto
            shortest_path_str = ' -> '.join(shortest_path_nodes)
            messagebox.showinfo("Camino más corto", f"El camino más corto entre los nodos {start_node} y {end_node} es: {shortest_path_str}")
            
            # Restaurar el color original de las aristas despues de cerrar el messagebox
            self.restore_edge_colors()
        else:
            messagebox.showinfo("Camino más corto", f"No hay camino entre los nodos {start_node} y {end_node}.")


    # Pinta las aristas mostrando el camino mas corto
    def highlight_shortest_path(self, shortest_path_nodes):
        for i in range(len(shortest_path_nodes) - 1):
            node1 = shortest_path_nodes[i]
            node2 = shortest_path_nodes[i + 1]
            edge = (node1, node2) if self.graph.has_edge(node1, node2) else (node2, node1)
            self.highlight_edge(edge,"red")


    # Pinta una arista especifica de rojo
    def highlight_edge(self, edge, color):
        # edge es una tupla que representa una arista (nodo1, nodo2)
        # color es el color con el que se quiere resaltar la arista
        if edge in self.graph_edges:
            self.canvas.itemconfig(self.graph_edges[edge], fill=color)
        else:
            # Si la arista no este en el diccionario, intentamos invertir los nodos en la tupla
            reversed_edge = (edge[1], edge[0])
            if reversed_edge in self.graph_edges:
                self.canvas.itemconfig(self.graph_edges[reversed_edge], fill=color)
            else:
                # Si la arista no se encuentra, imprimir un mensaje de advertencia
                print(f"La arista {edge} no se encontró en el diccionario de aristas.")


    # Restaura las aristas a su color original
    def restore_edge_colors(self):
        for edge in self.edges:
            self.canvas.itemconfig(self.graph_edges[edge], fill="black")


    # verifica si el grafo tiene un camino de Euler
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


    # mostrar el camino de Euler si existe
    def show_eulerian_path(self):
        is_eulerian, euler_path = self.eulerian_path()
        if is_eulerian:
            path_str = ' -> '.join(f"{edge[0]}-{edge[1]}" for edge in euler_path)
            messagebox.showinfo("Camino de Euler", f"El grafo tiene un camino de Euler:\n{path_str}")
        else:
            messagebox.showinfo("Camino de Euler", "El grafo no tiene un camino de Euler.")


    # Limpiar el lienzo
    def clear_canvas(self):
        self.canvas.delete("all")
        self.nodes = {}
        self.edges = []
        self.graph.clear()


    # Borrar un nodo seleccionado
    def delete_selected_node(self):
        if self.selected_node is not None:
            # Eliminar las aristas asociadas al nodo seleccionado del lienzo y del diccionario
            edges_to_delete = [(n1, n2) for n1, n2 in self.edges if n1 == self.selected_node or n2 == self.selected_node]
            for edge in edges_to_delete:
                self.canvas.delete(self.graph_edges[edge])  # Eliminar la arista del lienzo
                del self.graph_edges[edge]  # Eliminar la referencia de la arista del diccionario

            # Eliminar el nodo seleccionado y sus aristas del grafo
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

    # Crear un Frame para los botones
    button_frame = tk.Frame(root)
    button_frame.pack(side=tk.BOTTOM, fill=tk.X)  

    # Crear un Frame para los botones de arriba
    top_button_frame = tk.Frame(root)
    top_button_frame.pack(side=tk.TOP, fill=tk.X)  
    
    # Botón para mostrar información del grafo
    button_info = tk.Button(top_button_frame, text="Información del Grafo", command=app.show_graph_info)
    button_info.pack(side=tk.LEFT, padx=5, pady=5)  
    
    # Botón para mostrar el camino más corto
    button_shortest_path = tk.Button(button_frame, text="Camino más corto", command=app.show_shortest_path)
    button_shortest_path.pack(side=tk.RIGHT, padx=5, pady=5)  
    
    # Botón para mostrar el camino de Euler
    button_eulerian_path = tk.Button(button_frame, text="Camino de Euler", command=app.show_eulerian_path)
    button_eulerian_path.pack(side=tk.RIGHT, padx=5, pady=5)  
    
    # Botón para limpiar el lienzo
    clear_button = tk.Button(top_button_frame, text="Limpiar", command=app.clear_canvas)
    clear_button.pack(side=tk.RIGHT, padx=5, pady=5)  
    
    # Botón para eliminar un nodo
    delete_button = tk.Button(top_button_frame, text="Eliminar Nodo", command=app.delete_selected_node)
    delete_button.pack(side=tk.RIGHT, padx=5, pady=5)  

    # Botón para mostrar la matriz de adyacencia
    adjacency_matrix_button = tk.Button(button_frame, text="Matriz de Adyacencia", command=app.show_adjacency_matrix)
    adjacency_matrix_button.pack(side=tk.LEFT, padx=5, pady=5)

    # Botón para mostrar la matriz de incidencia
    incidence_matrix_button = tk.Button(button_frame, text="Matriz de Incidencia", command=app.show_incidence_matrix)
    incidence_matrix_button.pack(side=tk.LEFT, padx=5, pady=5)

    # Botón para mostrar los nodos del grafo
    button_nodes = tk.Button(button_frame, text="Nodos", command=app.show_graph_nodes)
    button_nodes.pack(side=tk.LEFT, padx=5, pady=5)  
    
    # Botón para mostrar las aristas del grafo
    button_edges = tk.Button(button_frame, text="Aristas", command=app.show_graph_edges)
    button_edges.pack(side=tk.LEFT, padx=5, pady=5)  

    # Botón para mostrar los vecinos de un nodo
    button_show_neighbors = tk.Button(button_frame, text="Vecinos", command=app.show_node_neighbors)
    button_show_neighbors.pack(side=tk.LEFT, padx=5, pady=5)  

    # Botón para mostrar el grado de un nodo
    button_show_degree = tk.Button(button_frame, text="Grado Nodo", command=app.show_node_degree)
    button_show_degree.pack(side=tk.LEFT, padx=5, pady=5)  

    root.mainloop()
    