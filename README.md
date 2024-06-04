# Gesture-Controlled Image Manipulation

A gesture-controlled image manipulation program that uses OpenCV to track the user's hand and MediaPipe to detect hand landmarks. The program can detect and track the user's hand in real-time.

## Functionality and Features
- Adjust the following parameters in live video:
  - Brightness
  - Contrast
  - Saturation
  - Sharpness
  - Blur
- Real-time hand tracking
- Adjust parameters by moving the index finger and thumb closer or farther apart

## Installation Instructions
- Python 3.8
- OpenCV
- MediaPipe
- NumPy
- PyQt5

## Setup Environment

### For Linux/Mac

1. **Install `venv`**:
    ```bash
    sudo apt-get install python3.8-venv
    ```

2. **Create virtual environment**:
    ```bash
    python3 -m venv env
    ```

3. **Activate virtual environment**:
    ```bash
    source env/bin/activate
    ```

### For Windows

1. **Install `venv`**:
    ```shell
    py -m pip install --user virtualenv
    ```

2. **Create virtual environment**:
    ```shell
    py -m venv env
    ```

3. **Activate virtual environment**:
    ```shell
    .\env\Scripts\activate
    ```

## Setup

Install the required libraries:
```bash
pip3 install -r requirements.txt
```

## Run

Execute the main script:
```bash
python src/main.py
```
