# AI Bicep Curl Tracker 🏋️‍♂️🤖

A real-time, computer vision-based fitness tracker that counts bicep curls using your webcam. Built with OpenCV and Google's MediaPipe Pose Estimation.

## 🌟 Features
* **Bilateral Tracking:** Tracks and counts repetitions for both the left and right arms simultaneously using Object-Oriented Programming (OOP).
* **Dynamic Angle Calculation:** Computes the exact angle of the elbow joint in real-time using NumPy vector math.
* **Smart State Machine:** Accurately counts a full repetition only when the arm fully extends (>150°) and fully contracts (<50°).
* **AI "Blindness" Protection:** Includes visibility thresholding (>50% confidence) to prevent false counting when joints are occluded or leave the camera frame.
* **Immersive UI:** Runs in a distraction-free, full-screen mode with dynamic on-screen data.

## 🛠️ Tech Stack
* **Python 3**
* **OpenCV:** Video capturing, frame rendering, and UI elements.
* **MediaPipe:** Advanced neural network for pose estimation and 3D landmark tracking.
* **NumPy:** Trigonometric math (`arctan2`) for joint angle calculation.

## ⚙️ Installation

1. Clone the repository (or download the source code):
   ```bash
   git clone https://github.com/Olat1337/bicep-curl-tracker.git
   cd bicep-curl-tracker

2. Create and activate a virtual environment (recommended):
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Linux/Mac
    # venv\Scripts\activate   # On Windows

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt

## Controls & Tips:

Ensure your room is well-lit.

Stand far enough back so your upper body (shoulders, elbows, and wrists) is visible to the camera.

Press the ESC key to safely exit the application.

## 🧠 How It Works

The script utilizes MediaPipe to extract 33 coordinate landmarks of the human body. We specifically extract the SHOULDER, ELBOW, and WRIST coordinates. By applying the inverse tangent function, the program calculates the relative angle between these three points. A custom Python class (BicepCurlCounter) independently manages the internal state ("up" or "down") for both the left and right sides of the body.
