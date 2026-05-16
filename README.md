# Hand Gesture Mouse Control

Control your mouse cursor using hand gestures detected via your webcam — no physical mouse required.

## Demo

| Gesture | Action |
|---|---|
| Thumb + Index finger pinch | Move cursor |
| Thumb + Middle finger pinch | Hold (drag) |
| Thumb + Ring finger pinch | Left click |

## How It Works

The script uses **MediaPipe** to detect hand landmarks in real time from the webcam feed. Three pinch combinations between the thumb and other fingers are mapped to mouse actions via **PyAutoGUI**. A lerp-based smoothing filter reduces jitter during cursor movement.

## Requirements

- Python 3.8+
- Webcam

Install dependencies:

```bash
pip install opencv-python mediapipe pyautogui numpy
```

## Usage

```bash
python no_mouse_move.py
```

Press `Q` to quit.

## Configuration

At the top of the script you can tune three threshold values (normalized 0–1 distance between fingertips):

```python
THRESH_MOVE  = 0.06   # thumb-index pinch sensitivity
THRESH_DRAG  = 0.06   # thumb-middle pinch sensitivity
THRESH_CLICK = 0.06   # thumb-ring pinch sensitivity
```

Decrease the value to require a tighter pinch; increase it to trigger more loosely.

The smoothing factor (`smoothing = 0.2`) controls cursor responsiveness — closer to `1.0` is more responsive but jittery, closer to `0.0` is smoother but sluggish.

## Tech Stack

- [OpenCV](https://opencv.org/) — webcam capture and display
- [MediaPipe](https://mediapipe.dev/) — real-time hand landmark detection
- [PyAutoGUI](https://pyautogui.readthedocs.io/) — cross-platform mouse control
- [NumPy](https://numpy.org/) — vector math for landmark distances and smoothing
