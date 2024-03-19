import cv2
import os
import numpy as np
import networkx as nx

def interpretar_grafo(imagen):
    # Convertir la imagen a escala de grises
    gray = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

    # Detección de círculos y líneas
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp=1, minDist=50, param1=200, param2=30, minRadius=15, maxRadius=45)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    # Detección de líneas utilizando la transformada de Hough probabilística
    lines = cv2.HoughLines(edges, rho=1, theta=np.pi/180, threshold=100)

    # Crear un grafo vacío
    G = nx.Graph()

    # Agregar nodos al grafo
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            G.add_node((i[0], i[1]))

    # Agregar aristas al grafo
    if lines is not None:
        for line in lines:
            rho, theta = line[0]
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            x1 = int(x0 + 1000 * (-b))
            y1 = int(y0 + 1000 * (a))
            x2 = int(x0 - 1000 * (-b))
            y2 = int(y0 - 1000 * (a))
            node1 = (x1, y1)
            node2 = (x2, y2)
            if node1 in G.nodes and node2 in G.nodes:
                G.add_edge(node1, node2)

    return G

# Ejemplo de uso
if __name__ == "__main__":
    imagen_path = "./preProcessedImages/preprocesada_g1.png"  # Reemplaza esto con la ruta de tu imagen procesada
    imagen_procesada = cv2.imread(imagen_path)
    grafo = interpretar_grafo(imagen_procesada)

    # Visualizar el grafo
    print("Nodos del grafo:", grafo.nodes)
    print("Aristas del grafo:", grafo.edges)

    # También puedes visualizar el grafo utilizando NetworkX
    import matplotlib.pyplot as plt
    nx.draw(grafo, with_labels=True)
    plt.show()