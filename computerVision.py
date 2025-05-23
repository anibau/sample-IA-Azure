# test_vision_all_services.py

import os
import time
from dotenv import load_dotenv

# Cliente Vision
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
# Modelos y constantes
from azure.cognitiveservices.vision.computervision.models import (
    VisualFeatureTypes,
    OperationStatusCodes,
    #FaceAttributeType
)
from msrest.authentication import CognitiveServicesCredentials

# Para dibujo y visualización
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt

# ————————————————————————————————————————
# 1. Configuración inicial
# ————————————————————————————————————————

# Carga variables de entorno (.env)
load_dotenv(".env")
ENDPOINT = os.getenv("VISION_ENDPOINT")
KEY      = os.getenv("VISION_KEY")

if not ENDPOINT or not KEY:
    raise RuntimeError("Define VISION_ENDPOINT y VISION_KEY en tu .env")

# Crea el cliente
vision_client = ComputerVisionClient(
    ENDPOINT,
    CognitiveServicesCredentials(KEY)
)

# Ruta de testeos
IMAGE_PATH = "./img/Lincoln.jpg"  # pon aquí tu imagen local

# ————————————————————————————————————————
# 2. Funciones de prueba
# ————————————————————————————————————————

def describe_image(path):
    """Describe la escena de la imagen (captions)."""
    with open(path, "rb") as img:
        desc = vision_client.describe_image_in_stream(img, max_candidates=3)
    print("\n=== Descripción de la imagen ===")
    for c in desc.captions:
        print(f" • '{c.text}' (confianza: {c.confidence:.2f})")

def tag_image(path):
    """Obtiene etiquetas (tags) de la imagen."""
    with open(path, "rb") as img:
        tags = vision_client.tag_image_in_stream(img)
    print("\n=== Etiquetas detectadas ===")
    for t in tags.tags:
        print(f" • {t.name} (confianza: {t.confidence:.2f})")

def detect_objects(path):
    """Detecta objetos y dibuja recuadros sobre la imagen."""
    with open(path, "rb") as img:
        objs = vision_client.detect_objects_in_stream(img)
    print("\n=== Objetos detectados ===")
    image = Image.open(path)
    draw  = ImageDraw.Draw(image)
    for o in objs.objects:
        rect = o.rectangle
        print(f" • {o.object_property} (confianza: {o.confidence:.2f}) en {rect}")
        # dibujar caja y etiqueta
        draw.rectangle(
            [(rect.x, rect.y), (rect.x + rect.w, rect.y + rect.h)],
            outline="cyan", width=3
        )
        draw.text((rect.x, rect.y - 10), o.object_property, fill="cyan")
    plt.axis("off")
    plt.imshow(image)
    plt.show()

def read_text(path):
    """Realiza OCR (Read API) y muestra texto detectado."""
    with open(path, "rb") as img:
        read_op = vision_client.read_in_stream(img, raw=True)
    # Obtener Operation-Location y extraer ID
    op_loc = read_op.headers["Operation-Location"]
    op_id  = op_loc.split("/")[-1]
    # Polling hasta terminar
    while True:
        result = vision_client.get_read_result(op_id)
        if result.status not in ['notStarted', 'running']:
            break
        time.sleep(1)
    print("\n=== Texto reconocido (OCR) ===")
    if result.status == OperationStatusCodes.succeeded:
        for page in result.analyze_result.read_results:
            for line in page.lines:
                print(f" • {line.text}")
    else:
        print("OCR falló con estado:", result.status)

# def detect_faces(path):
#     """Detecta rostros y muestra edad y género."""
#     with open(path, "rb") as img:
#         faces = vision_client.detect_faces_in_stream(
#             img,
#             return_face_attributes=[FaceAttributeType.age, FaceAttributeType.gender]
#         )
#     print("\n=== Rostros detectados ===")
#     for f in faces:
#         rect = f.face_rectangle
#         attrs = f.face_attributes
#         print(f" • Rostro en {rect}: edad={attrs.age}, género={attrs.gender}")

# ————————————————————————————————————————
# 3. Ejecutar todas las pruebas
# ————————————————————————————————————————

if __name__ == "__main__":
    describe_image(IMAGE_PATH)
    tag_image(IMAGE_PATH)
    detect_objects(IMAGE_PATH)
    read_text(IMAGE_PATH)
   # detect_faces(IMAGE_PATH)
