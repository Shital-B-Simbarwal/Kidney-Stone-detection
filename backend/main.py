
from pathlib import Path

import torch
import torch.nn as nn
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from torchvision import models, transforms
from io import BytesIO

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "src" / "kidney_stone_model.pth"

# App setup
app = FastAPI(title="KidneyScan API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

device = torch.device("cpu")

# Must match the architecture used during training
model = models.mobilenet_v2(weights=None)
model.classifier[1] = nn.Linear(
    model.last_channel, 1
)

try:
    state_dict = torch.load(
        MODEL_PATH,
        map_location=device,
        weights_only=True,
    )
    model.load_state_dict(state_dict)
    model.eval()
except Exception as exc:
    raise RuntimeError(
        f"Could not load model from {MODEL_PATH}: {exc}"
    ) from exc

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225],
    ),
])


@app.get("/")
def home():
    return {"message": "KidneyScan API is running"}


@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": True}


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    if file.content_type not in {
        "image/jpeg",
        "image/png",
        "image/jpg",
    }:
        raise HTTPException(
            status_code=400,
            detail="Please upload a JPG or PNG image.",
        )

    try:
        contents = await file.read()

        if len(contents) > 10 * 1024 * 1024:
            raise HTTPException(
                status_code=413,
                detail="Image must be smaller than 10 MB.",
            )

        image = Image.open(BytesIO(contents)).convert("RGB")
        tensor = transform(image).unsqueeze(0).to(device)

        with torch.inference_mode():
            logit = model(tensor)
            probability = torch.sigmoid(logit).item()

        # ImageFolder classes are alphabetically ordered:
        # normal = 0, stone = 1, if those are the training folders.
        prediction = (
            "Stone" if probability >= 0.5 else "Normal"
        )

        return {
            "prediction": prediction,
            "stone_probability": round(probability, 4),
            "confidence_percent": round(
                max(probability, 1 - probability) * 100, 2
            ),
            "message": (
                "Educational prototype only—not a medical diagnosis."
            ),
        }

    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail=f"Could not process image: {exc}",
        ) from exc
