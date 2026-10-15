
import os
import sys
import torch
import torch.nn as nn
from PIL import Image
from torchvision import models, transforms

# Get the project paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(os.path.dirname(__file__), "kidney_stone_model.pth")

# Use CPU or GPU automatically
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Image preprocessing must match training.py
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        [0.485, 0.456, 0.406],
        [0.229, 0.224, 0.225]
    )
])


def load_model():
    """Load the trained MobileNetV2 model."""
    model = models.mobilenet_v2(weights=None)
    model.classifier[1] = nn.Linear(model.last_channel, 1)

    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            f"Model file not found: {MODEL_PATH}"
        )

    state_dict = torch.load(
        MODEL_PATH,
        map_location=DEVICE,
        weights_only=True
    )

    model.load_state_dict(state_dict)
    model.to(DEVICE)
    model.eval()

    return model


def predict_image(image_path, model):
    """Predict whether an image belongs to the normal or stone class."""
    if not os.path.isfile(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    with Image.open(image_path) as image:
        image = image.convert("RGB")
        image_tensor = transform(image).unsqueeze(0).to(DEVICE)

    with torch.no_grad():
        output = model(image_tensor)
        stone_probability = torch.sigmoid(output).item()

    # ImageFolder normally assigns alphabetical class indices:
    # normal = 0, stone = 1.
    # Confirm this matches your training dataset.
    if stone_probability >= 0.5:
        prediction = "Stone"
        confidence = stone_probability * 100
    else:
        prediction = "Normal"
        confidence = (1 - stone_probability) * 100

    return {
        "prediction": prediction,
        "confidence": round(confidence, 2),
        "stone_probability": round(stone_probability * 100, 2)
    }


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python src/predict.py <image_path>")
        sys.exit(1)

    try:
        model = load_model()
        result = predict_image(sys.argv[1], model)

        print("\n--- Kidney Stone Detection Result ---")
        print(f"Prediction: {result['prediction']}")
        print(f"Confidence: {result['confidence']}%")
        print(f"Stone probability: {result['stone_probability']}%")
        print("\nEducational prototype only—not a medical diagnosis.")

    except Exception as error:
        print(f"Error: {error}")
        sys.exit(1)
