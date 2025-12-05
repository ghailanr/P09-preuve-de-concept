import os
import joblib
from fastapi import FastAPI
from utils import download_if_needed

app = FastAPI()

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
