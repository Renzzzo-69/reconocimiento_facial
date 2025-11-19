import cv2
import os
import sys

# Crear carpeta para guardar imágenes del usuario
#nombre = input("Nombre del usuario a registrar: ")
nombre = sys.argv[1]

path = f"dataset/{nombre}"
os.makedirs(path, exist_ok=True)

cam = cv2.VideoCapture(1)
count = 0

print("\nPresiona 'c' para capturar fotos. Se guardarán 90 imágenes.\n")

while True:
    ret, frame = cam.read()
    if not ret:
        break
    
    cv2.imshow("Capturando rostro", frame)

    # Capturar imagen con tecla 'c'
    if cv2.waitKey(1) & 0xFF == ord('c'):
        cv2.imwrite(f"{path}/{count}.jpg", frame)
        print(f"Imagen guardada: {count}.jpg")
        count += 1

    # Guardar 90 imágenes por usuario
    if count == 90: 
        print("\n✔ Captura completa!")
        break

    # Salir con 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
