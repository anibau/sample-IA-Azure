// Cargar variables de entorno desde .env
require("dotenv").config();

const { AzureKeyCredential } = require("@azure/core-auth");
const createClient = require("@azure-rest/ai-vision-image-analysis").default;

const endpoint = process.env['VISION_ENDPOINT'] || '<your_endpoint>';
const key = process.env['VISION_KEY'] || '<your_key>';

const credential = new AzureKeyCredential(key);
const client = createClient(endpoint, credential);

const imageUrl = 'https://learn.microsoft.com/azure/ai-services/computer-vision/media/quickstarts/presentation.png';

const features = ['Objects', 'People'];

async function main() {
  try {
    const result = await client.path("/imageanalysis:analyze").post({
      body: {
        url: imageUrl,
      },
      queryParameters: {
        features: features.join(','), // ✅ Debe ser string, no array directamente
        language: 'en',
        'gender-neutral-captions': 'true',
        'smartCrops-aspect-ratios': [0.9, 1.33],
      },
      contentType: 'application/json',
    });

    console.log("Resultado:");
    console.dir(result.body, { depth: null });
  } catch (error) {
    console.error("Error al analizar la imagen:", error);
  }
}

main();
