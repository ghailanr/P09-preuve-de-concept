import joblib
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from azure.storage.blob import BlobClient
import hashlib
import os

app = FastAPI()

AZURE_STORAGE_KEY = os.getenv("AZURE_STORAGE_KEY")
CONTAINER_NAME = "models"

LOCAL_DIR = "models"
os.makedirs(LOCAL_DIR, exist_ok=True)

FILES = {
    "model.pkl": os.path.join(LOCAL_DIR, "model.pkl"),
    "tokenizer.pkl": os.path.join(LOCAL_DIR, "tokenizer.pkl"),
}

def sha256_file(path):
    """Retourne le hash SHA256 d'un fichier local."""
    if not os.path.exists(path):
        return None
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()

def sha256_blob(blob):
    """Retourne le hash SHA256 d'un blob Azure (en streaming)."""
    h = hashlib.sha256()
    stream = blob.download_blob().chunks()
    for chunk in stream:
        h.update(chunk)
    return h.hexdigest()

def download_if_needed(filename, local_path):
    blob = BlobClient.from_connection_string(
        conn_str=AZURE_STORAGE_KEY,
        container_name=CONTAINER_NAME,
        blob_name=filename
    )

    print(f"\n[INFO] Vérification du cache pour {filename}")

    remote_hash = sha256_blob(blob)
    local_hash = sha256_file(local_path)

    if local_hash == remote_hash:
        print(f"[CACHE] {filename} inchangé → pas de téléchargement.")
        return

    print(f"[DOWNLOAD] Téléchargement de {filename}...")
    with open(local_path, "wb") as f:
        f.write(blob.download_blob().readall())
    print(f"[INFO] {filename} mis à jour.")


class TextInput(BaseModel):
    text: str

@app.on_event("startup")
def load_artifacts():
    global model, tokenizer

    for filename, local_path in FILES.items():
        download_if_needed(filename, local_path)

    print("\n[INFO] Chargement du modèle...")
    model = joblib.load(FILES["model.pkl"])
    tokenizer = joblib.load(FILES["tokenizer.pkl"])
    print("[INFO] Modèle et tokenizer chargés.")

@app.get("/")
def root():
    return {"status": "API ok", "cache": "enabled"}

@app.post("/predict")
async def predict(text: TextInput):
    print("WIP")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

