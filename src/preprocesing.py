import cv2
import os

def preprocesar_imagen(image_path):
    # Cargar la imagen
    imagen = cv2.imread(image_path)

    # Convertir la imagen a escala de grises
    imagen_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

    # Aplicar umbralización adaptativa para segmentar la imagen
    _, imagen_umbralizada = cv2.threshold(imagen_gris, 100, 255, cv2.THRESH_BINARY)

    # Aplicar detección de bordes utilizando el algoritmo Canny
    imagen_bordes = cv2.Canny(imagen_umbralizada, 50, 150)

    # Dilatación de la imagen de bordes
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    imagen_bordes_dilatada = cv2.dilate(imagen_bordes, kernel, iterations=1)

    # Detección de líneas utilizando la transformada de Hough
    lineas = cv2.HoughLinesP(imagen_bordes_dilatada, 1, 3.14/180, threshold=50, minLineLength=50, maxLineGap=5)  # Adjusted parameters

    if lineas is not None:
        # Dibujar las líneas encontradas (aristas)
        for linea in lineas:
            x1, y1, x2, y2 = linea[0]
            cv2.line(imagen, (x1, y1), (x2, y2), (0, 0, 0), 10)  # Aumentar el grosor de la lí

    # Detección de nodos (círculos) utilizando la transformada de Hough circular
    circulos = cv2.HoughCircles(imagen_gris, cv2.HOUGH_GRADIENT, dp=1, minDist=50, param1=100, param2=30, minRadius=2, maxRadius=400)

    if circulos is not None:
        # Dibujar los círculos encontrados (nodos)
        for circulo in circulos[0]:
            centro = (int(circulo[0]), int(circulo[1]))
            radio = int(circulo[2])

            # Dibujar el nodo con relleno azul
            cv2.circle(imagen, centro, radio, (255, 0, 0), -1)

    # Guardar la imagen preprocesada
    directorio_salida = "./preProcessedImages"
    nombre_archivo = os.path.basename(image_path)
    ruta_salida = os.path.join(directorio_salida, "preprocesada_" + nombre_archivo)
    cv2.imwrite(ruta_salida, imagen)

    return imagen

# Ejemplo de uso
if __name__ == "__main__":
    imagen_path = "./processedImages/ej2.jpeg"  # Reemplaza esto con la ruta de tu imagen de grafo
    imagen_preprocesada = preprocesar_imagen(imagen_path)

    # Redimensionar la ventana de visualización según el tamaño de la imagen
    cv2.namedWindow("Imagen preprocesada", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Imagen preprocesada", imagen_preprocesada.shape[1], imagen_preprocesada.shape[0])

    cv2.imshow("Imagen preprocesada", imagen_preprocesada)
    cv2.waitKey(0)
    cv2.destroyAllWindows()