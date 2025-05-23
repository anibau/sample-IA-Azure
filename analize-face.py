# Import namespaces
from azure.ai.vision.face import FaceClient
from azure.cognitiveservices.vision.face import FaceClient

from azure.ai.vision.face.models import FaceDetectionModel, FaceRecognitionModel, FaceAttributeTypeDetection01
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
import os
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt

# Cargar variables de entorno
load_dotenv(".env")
endpoint = os.getenv("FACE_ENDPOINT")
key = os.getenv("FACE_KEY")
if not endpoint or not key:
    raise RuntimeError("FACE_ENDPOINT y FACE_KEY deben estar definidas")

# Crear cliente Face
face_client = FaceClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(key)
)

# Atributos que se desean detectar
features = [
    FaceAttributeTypeDetection01.HEAD_POSE,
    FaceAttributeTypeDetection01.OCCLUSION,
    FaceAttributeTypeDetection01.ACCESSORIES
]

# Ruta de la imagen
image_file = "./img/person.jpg"
# ———————————————————————————————————
# ✅ Definición de la función annotate_faces
# ———————————————————————————————————
def annotate_faces(image_path, face_results):
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)

    for face in face_results:
        r = face.face_rectangle
        left = r.left
        top = r.top
        right = r.left + r.width
        bottom = r.top + r.height

        # Dibujar rectángulo alrededor del rostro
        draw.rectangle(((left, top), (right, bottom)), outline="lime", width=3)
        draw.text((left, top - 10), f"Face", fill="lime")

    # Mostrar imagen con matplotlib
    plt.figure(figsize=(8, 6))
    plt.axis("off")
    plt.imshow(image)
    plt.show()

# Detectar rostros
with open(image_file, mode="rb") as image_data:
    detected_faces = face_client.detect(
        image_content=image_data.read(),
        detection_model=FaceDetectionModel.DETECTION01,
        recognition_model=FaceRecognitionModel.RECOGNITION01,
        return_face_id=False,
        return_face_attributes=features,
    )

# Mostrar propiedades de rostros
face_count = 0
if len(detected_faces) > 0:
    print(len(detected_faces), 'rostros detectados.')
    for face in detected_faces:
        face_count += 1
        print(f'\nRostro #{face_count}')
        print(f' - Head Pose (Yaw): {face.face_attributes.head_pose.yaw}')
        print(f' - Head Pose (Pitch): {face.face_attributes.head_pose.pitch}')
        print(f' - Head Pose (Roll): {face.face_attributes.head_pose.roll}')
        print(f' - Forehead occluded?: {face.face_attributes.occlusion["foreheadOccluded"]}')
        print(f' - Eye occluded?: {face.face_attributes.occlusion["eyeOccluded"]}')
        print(f' - Mouth occluded?: {face.face_attributes.occlusion["mouthOccluded"]}')
        print(' - Accessories:')
        for accessory in face.face_attributes.accessories:
            print(f'   - {accessory.type}')

    # ✅ Llamar a la función para dibujar los rostros
    annotate_faces(image_file, detected_faces)

else:
    print("No se detectaron rostros.")


