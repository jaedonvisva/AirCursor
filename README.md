# Hand Gesture Control System

This project is a **real-time hand gesture recognition system** that maps hand movements and gestures to desktop actions such as mouse control, scrolling, and clicking. It leverages computer vision and machine learning technologies to enable intuitive, hardware-free human-computer interaction using only a webcam.

---

## Features

- **Real-time Hand Tracking**: Detects and tracks hands in video frames using Mediapipe.
- **Mouse Control**: Use your hand to move the mouse cursor on the screen.
- **Scrolling Gestures**: Perform scrolling actions (up/down) with pinch gestures.
- **Click Detection**: Simulate mouse clicks using specific hand gestures.
- **High Performance**: Achieves real-time responsiveness with an average FPS of 30+.

---

## Technologies Used

- **[OpenCV](https://opencv.org/)**: For video processing and accessing the webcam.
- **[Mediapipe](https://mediapipe.dev/)**: For advanced hand detection and gesture tracking.
- **[PyAutoGUI](https://pyautogui.readthedocs.io/)**: To control mouse and scrolling actions programmatically.
- **Math Library**: For calculating distances between landmarks for gesture detection.
- **Time Library**: To measure and display performance metrics (frames per second).

---

## How It Works

1. **Hand Detection**: Mediapipe detects the hand and landmarks in each frame captured by the webcam.
2. **Gesture Recognition**: Landmarks are analyzed to determine finger positions and gestures.
   - **Thumb and Index Finger Pinch**: Scrolls down.
   - **Thumb and Middle Finger Pinch**: Scrolls up.
   - **All Fingers Down**: Simulates a left mouse click.
3. **Mouse Movement**: The index finger's position maps to the screen coordinates, controlling the mouse cursor.

---

## Requirements

- Python 3.7 or later
- Libraries: 
  - OpenCV
  - Mediapipe
  - PyAutoGUI
  - Math (built-in)
  - Time (built-in)

Install required libraries using:
```bash
pip install opencv-python mediapipe pyautogui
