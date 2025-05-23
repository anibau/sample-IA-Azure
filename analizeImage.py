
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
import os
load_dotenv(".env")

endpoint = os.getenv("VISION_ENDPOINT")
key      = os.getenv("VISION_KEY")
if not endpoint or not key:
    raise RuntimeError("VISION_ENDPOINT y VISION_KEY deben estar definidas")

client = ImageAnalysisClient(
    endpoint= endpoint,
    credential=AzureKeyCredential(key)
)

try: 
    with open("./img/building.jpg", "rb") as f:

        result = client.analyze(
            image_data= f,
            visual_features=[VisualFeatures.CAPTION, VisualFeatures.READ, VisualFeatures.TAGS, VisualFeatures.OBJECTS, VisualFeatures.PEOPLE, VisualFeatures.DENSE_CAPTIONS],
            gender_neutral_caption=True,
            language="en",
        )
    for tag in result.tags:
        print("Etiquetas detectadas:")
        print(result.tags)
        print("descripciones detectadas:")
        print(result.caption)

except Exception as e:
    print("Error analizando la imagen:", e)
    

# Display analysis results
# Get image captions
if result.caption is not None:
    print("\nCaption:")
    print(" Caption: '{}' (confidence: {:.2f}%)".format(result.caption.text, result.caption.confidence * 100))

# Get image dense captions
if result.dense_captions is not None:
    print("\nDense Captions:")
    for caption in result.dense_captions.list:
        print(" Caption: '{}' (confidence: {:.2f}%)".format(caption.text, caption.confidence * 100))

# Get image tags


# Get objects in the image


    

# Get people in the image

