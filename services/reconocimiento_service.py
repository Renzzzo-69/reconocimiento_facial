from utils.detector_api import reconocer_imagen

def reconocer(file_path):
    id_usuario = reconocer_imagen(file_path)
    return id_usuario
