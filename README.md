# Kidney Stone Detection Using Deep Learning

A deep learning project that classifies CT scan images into two categories: **Normal** and **Kidney Stone**, using PyTorch.

## Project Overview

This project explores medical image classification using a convolutional neural network (CNN). The model is trained on CT scan images to distinguish between normal scans and scans containing kidney stones.

## Tech Stack

- **Language:** Python
- **Deep Learning:** PyTorch, Torchvision
- **Image Processing:** Pillow, NumPy

## Project Structure

```text
kidney-stone-detection/
├── Data/
│   ├── train/
│   │   ├── normal/
│   │   └── stone/
├── src/
│   ├── training.py
│   └── kidney_stone_model.pth
├── requirements.txt
└── .gitignore
```

*Note: The dataset is not included in this repository.*

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Shital-B-Simbarwal/kidney-stone-detection.git
   cd kidney-stone-detection
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   ```

   Windows:

   ```bash
   venv\Scripts\activate
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Model and Training

- `src/training.py` contains the model training code.
- `src/kidney_stone_model.pth` contains the saved model weights.
- The dataset is organized into `normal` and `stone` classes.

## Future Improvements

- Add an image prediction script.
- Evaluate the model using accuracy, precision, recall, and a confusion matrix.
- Develop a simple web interface for image classification.

## Disclaimer

This project is intended for educational purposes only. It is not a clinically validated diagnostic tool and must not be used to diagnose or make medical decisions.
