import face_recognition
import os
import pickle

DATASET_DIR = "dataset"
MODELS_DIR = "models"
ENCODINGS_PATH = os.path.join(MODELS_DIR, "encodings.pickle")

os.makedirs(MODELS_DIR, exist_ok=True)

print("\nEntrenando modelo...")

all_encodings = []
all_ids = []

for folder in os.listdir(DATASET_DIR):
    user_path = os.path.join(DATASET_DIR, folder)
    if not os.path.isdir(user_path):
        continue

    # 📌 la carpeta ES el ID del usuario
    try:
        user_id = int(folder)
    except:
        print(f"[!] La carpeta '{folder}' no es un ID. Se omite.")
        continue

    print(f"Procesando usuario ID: {user_id}")

    for img_name in os.listdir(user_path):
        image_path = os.path.join(user_path, img_name)

        try:
            image = face_recognition.load_image_file(image_path)
        except Exception as e:
            print(f"  [X] Error leyendo {image_path}: {e}")
            continue

        boxes = face_recognition.face_locations(image)
        if len(boxes) == 0:
            print(f"  [!] Sin rostro detectado en {img_name}, se omite.")
            continue

        encoding = face_recognition.face_encodings(image, boxes)[0]
        all_encodings.append(encoding)
        all_ids.append(user_id)

print(f"\nTotal encodings: {len(all_encodings)}")

if len(all_encodings) == 0:
    print("No se generaron encodings. Revisa tu dataset.")
else:
    data = {
        "encodings": all_encodings,
        "ids": all_ids
    }
    with open(ENCODINGS_PATH, "wb") as f:
        pickle.dump(data, f)

    print(f"\n✔ Modelo entrenado y guardado en {ENCODINGS_PATH}")
