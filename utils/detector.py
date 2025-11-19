import cv2
import face_recognition
import pickle
import numpy as np
import os

MODELS_DIR = "models"
ENCODINGS_PATH = os.path.join(MODELS_DIR, "encodings.pickle")

if not os.path.exists(ENCODINGS_PATH):
    print("No existe encodings.pickle. Entrena primero.")
    exit()

data = pickle.load(open(ENCODINGS_PATH, "rb"))
known_encodings = data["encodings"]
known_names = data["names"]

# Tolerancia más estricta
TOLERANCE = 0.45  

cam = cv2.VideoCapture(1)  # 0 = laptop, 1 = cámara del cel

print("\nSistema de reconocimiento facial iniciado.\nPresiona 'q' para salir.\n")

while True:
    ret, frame = cam.read()
    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    boxes = face_recognition.face_locations(rgb)
    encodings = face_recognition.face_encodings(rgb, boxes)

    for encoding, box in zip(encodings, boxes):
        # Calcular distancias con TODOS los encodings
        distances = face_recognition.face_distance(known_encodings, encoding)
        best_match_index = np.argmin(distances)
        best_distance = distances[best_match_index]

        # Debug opcional:
        # print("Mejor distancia:", best_distance, "→", known_names[best_match_index])

        if best_distance <= TOLERANCE:
            name = known_names[best_match_index]
        else:
            name = "DESCONOCIDO"

        top, right, bottom, left = box
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX,
                    0.8, (0, 255, 0), 2)

    cv2.imshow("Reconocimiento Facial", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
print("\nSistema de reconocimiento facial detenido.")