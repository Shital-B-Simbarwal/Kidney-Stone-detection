# Kidney Stone Detection Using Deep Learning

A deep learning project that classifies CT scan images into two categories: **Normal** and **Kidney Stone**, using PyTorch and MobileNetV2 transfer learning.

## Project Overview

This project explores medical image classification using a pretrained convolutional neural network (MobileNetV2). The model is trained on CT scan images to distinguish between normal scans and scans containing kidney stones.

The training script includes validation, loss and accuracy tracking, evaluation metrics, and saving the trained model weights.

## Tech Stack

- **Language:** Python
- **Deep Learning:** PyTorch, Torchvision
- **Image Processing:** Pillow, NumPy
- **Model Evaluation:** scikit-learn

## Project Structure

```text
kidney-stone-detection/
├── src/
│   ├── training.py
│   └── kidney_stone_model.pth
├── requirements.txt
├── README.md
└── .gitignore
```

**Note:** The dataset is not included in this repository. To train the model, organize the dataset into `Data/train/normal/` and `Data/train/stone/`.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Shital-B-Simbarwal/Kidney-Stone-detection.git
   cd Kidney-Stone-detection
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   ```

   On Windows:

   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Model Training and Evaluation

Run the training script from the project root:

```bash
python src/training.py
```

The script uses MobileNetV2 pretrained weights and trains a binary classifier. It reports training and validation loss and accuracy for each epoch, followed by evaluation metrics including accuracy, precision, recall, F1-score, and a confusion matrix.

The trained model weights are saved to:

`src/kidney_stone_model.pth`

**Note:** Training requires the dataset to be present in the expected directory structure. The script uses 80% of the available images for training and 20% for validation.

## Future Improvements

- Add a separate image prediction script.
- Improve evaluation and report verified model performance.
- Develop a simple web interface for image classification.

## Disclaimer

This project is intended for educational purposes only. It is not a clinically validated diagnostic tool and must not be used to diagnose or make medical decisions.
