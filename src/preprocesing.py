import cv2
import os

def preprocesar_imagen(image_path):
    # Cargar la imagen
    imagen = cv2.imread(image_path)

    # Convertir a escala de grises
    gray = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

    # Detección de círculos
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp=1, minDist=50, param1=200, param2=30, minRadius=0, maxRadius=0)

    # Dibujar círculos detectados
    if circles is not None:
        circles = circles.astype(int)
        for i in circles[0, :]:
            cv2.circle(imagen, (i[0], i[1]), i[2], (0, 255, 0), 2)

    # Detección de líneas
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    lines = cv2.HoughLinesP(edges, rho=1, theta=1 * (3.14 / 180), threshold=100, minLineLength=100, maxLineGap=10)

    # Dibujar líneas detectadas
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(imagen, (x1, y1), (x2, y2), (0, 0, 255), 2)

    # Guardar la imagen preprocesada
    directorio_salida = "./preProcessedImages"
    nombre_archivo = os.path.basename(image_path)
    ruta_salida = os.path.join(directorio_salida, "preprocesada_" + nombre_archivo)
    cv2.imwrite(ruta_salida, imagen)

    return imagen

# Ejemplo de uso
if __name__ == "__main__":
    imagen_path = "./processedImages/g1.png"  # Reemplaza esto con la ruta de tu imagen de grafo
    imagen_preprocesada = preprocesar_imagen(imagen_path)

    # Redimensionar la ventana de visualización según el tamaño de la imagen
    cv2.namedWindow("Imagen preprocesada", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Imagen preprocesada", imagen_preprocesada.shape[1], imagen_preprocesada.shape[0])

    cv2.imshow("Imagen preprocesada", imagen_preprocesada)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
 