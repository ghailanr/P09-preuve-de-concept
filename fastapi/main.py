import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class TextInput(BaseModel):
    text: str

@app.get("/")
def root():
    return {"status": "API ok", "cache": "enabled"}

@app.post("/predict")
async def predict(text: TextInput):
    print("WIP")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

