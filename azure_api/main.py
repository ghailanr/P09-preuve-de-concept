import uvicorn
import os
import pickle
from fastapi import FastAPI
from pydantic import BaseModel
from azure.storage.blob import BlobServiceClient

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

CONTAINER_NAME = "models"
MODEL_FILE = "modernBERT.pkl"
TOKENIZER_FILE = "modernBERT_tokenizer.pkl"

model = None
tokenizer = None

def download_blob_to_file(blob_service_client, blob_name, local_path):
    container = blob_service_client.get_container_client(CONTAINER_NAME)
    blob = container.get_blob_client(blob_name)

    with open(local_path, "wb") as f:
        data = blob.download_blob()
        f.write(data.readall())
    print(f"✔ Fichier téléchargé : {local_path}")


@app.on_event("startup")
def startup_event():
    global model, tokenizer

    logger.info("Loading ModernBERT model...")

    conn_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    if not conn_str:
        raise ValueError("AZURE_STORAGE_CONNECTION_STRING n'est pas configurée !")

    blob_service_client = BlobServiceClient.from_connection_string(conn_str)

    local_model_path = "/tmp/modernBERT.pkl"
    local_tokenizer_path = "/tmp/modernBERT_tokenizer.pkl"

    download_blob_to_file(blob_service_client, MODEL_FILE, local_model_path)
    download_blob_to_file(blob_service_client, TOKENIZER_FILE, local_tokenizer_path)

    with open(local_model_path, "rb") as f:
        model = pickle.load(f)

    with open(local_tokenizer_path, "rb") as f:
        tokenizer = pickle.load(f)

    logger.info("ModernBERT loaded!")

class TextInput(BaseModel):
    text: str

@app.get("/")
def root():
    return {"status": "API ok", "model_loaded": model is not None}

@app.post("/predict/")
async def predict(payload: TextInput):
    print("WIP - prédiction bientôt intégrée.")
    return {"text": payload.text, "prediction": "en cours"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

