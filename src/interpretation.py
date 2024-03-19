import cv2
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# Función para interpretar los resultados del preprocesamiento y extraer información útil del grafo
def interpretar_grafo(imagen_preprocesada):
    # Convertir la imagen preprocesada a escala de grises
    imagen_gris = cv2.cvtColor(imagen_preprocesada, cv2.COLOR_BGR2GRAY)

    # Detección de nodos (círculos azules)
    nodos = cv2.HoughCircles(imagen_gris, cv2.HOUGH_GRADIENT, dp=1, minDist=50, param1=50, param2=30, minRadius=5, maxRadius=30)

    # Detección de aristas (líneas rojas)
    bordes_rojos = cv2.inRange(imagen_preprocesada, np.array([0, 0, 150]), np.array([100, 100, 255]))
    contornos, _ = cv2.findContours(bordes_rojos, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Crear un grafo vacío
    grafo = nx.Graph()

    # Agregar nodos al grafo y asignar etiquetas y posiciones
    if nodos is not None:
        nodos = np.round(nodos[0, :]).astype("int")
        for i, (x, y, _) in enumerate(nodos):
            etiqueta_nodo = f"Nodo {i+1}"
            grafo.add_node(etiqueta_nodo, pos=(x, y))

    # Agregar aristas al grafo
    for contorno in contornos:
        if len(contorno) > 1:
            inicio = tuple(contorno[0][0])
            fin = tuple(contorno[-1][0])
            grafo.add_edge(inicio, fin)

    return grafo


# Ejemplo de uso
if __name__ == "__main__":
    imagen_preprocesada = cv2.imread("/home/joki/Documents/code/GraphsTheory/preProcessedImages/preprocesada_ej2.jpeg")  # Reemplaza esto con la imagen preprocesada
    grafo = interpretar_grafo(imagen_preprocesada)

    # Imprimir información del grafo
    print("Número de nodos:", grafo.number_of_nodes())
    print("Número de aristas:", grafo.number_of_edges())
    print("Nodos:", grafo.nodes())
    print("Aristas:", grafo.edges())

    # Visualizar el grafo
    posiciones_nodos = nx.get_node_attributes(grafo, 'pos')
    nx.draw(grafo, posiciones_nodos, with_labels=True, node_color='skyblue', node_size=500)
    plt.show()