import cv2
import face_recognition
import numpy as np
import pickle
import os

ENCODINGS_PATH = "models/encodings.pickle"

# Variables globales (se pueden recargar)
known_encodings = []
known_ids = []

TOLERANCE = 0.45

# ================================
# Función para recargar encodings
# ================================
def cargar_encodings():
    global known_encodings, known_ids

    if not os.path.exists(ENCODINGS_PATH):
        print("❌ No existe encodings.pickle")
        known_encodings = []
        known_ids = []
        return

    print("🔄 Recargando encodings...")
    data = pickle.load(open(ENCODINGS_PATH, "rb"))
    known_encodings = data["encodings"]
    known_ids = data["ids"]
    print(f"✔ Encodings cargados: {len(known_encodings)} rostros.")


# Cargar al arrancar el servidor
cargar_encodings()

# Cámara (solo si usas cámara, no afecta reconocimiento por imagen)
cam = cv2.VideoCapture(1)

def reconocer_imagen(ruta):
    try:
        image = face_recognition.load_image_file(ruta)
    except:
        return None

    boxes = face_recognition.face_locations(image)
    if len(boxes) == 0:
        return None

    encoding = face_recognition.face_encodings(image, boxes)[0]

    if len(known_encodings) == 0:
        print("⚠ No hay encodings cargados todavía.")
        return None

    distances = face_recognition.face_distance(known_encodings, encoding)
    best_match_index = np.argmin(distances)
    best_distance = distances[best_match_index]

    if best_distance <= TOLERANCE:
        return known_ids[best_match_index]
    else:
        return None
