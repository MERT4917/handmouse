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

## Installation

Follow these steps to get the project running on your machine:

**1. Clone the repository**
```bash
git clone https://github.com/your-username/mousemove.git
cd mousemove
```

**2. (Recommended) Create a virtual environment**
```bash
python -m venv venv
```
Activate it:
- Windows: `venv\Scripts\activate`
- macOS / Linux: `source venv/bin/activate`

**3. Install dependencies**
```bash
pip install opencv-python mediapipe pyautogui numpy
```

**4. Run the script**
```bash
python no_mouse_move.py
```

Press `Q` to quit.

> **Note:** On first launch (especially as a compiled `.exe`), the app may take **3–4 seconds** to open. This is normal — MediaPipe, OpenCV, and NumPy are large libraries that need time to load. A splash screen is shown during this period so you know the app is starting.

### Running as an Executable (Windows)

If you prefer not to install Python, you can build a standalone `.exe`:

```bash
pip install pyinstaller
pyinstaller --onefile --noconsole --collect-all mediapipe no_mouse_move.py
```

The executable will be created at `dist\no_mouse_move.exe`. Double-click to run — no Python installation required.

## Configuration

At the top of the script you can tune three threshold values (normalized 0–1 distance between fingertips):

```python
THRESH_MOVE  = 0.06   # thumb-index pinch sensitivity
THRESH_DRAG  = 0.06   # thumb-middle pinch sensitivity
THRESH_CLICK = 0.06   # thumb-ring pinch sensitivity
```

Decrease the value to require a tighter pinch; increase it to trigger more loosely.

The smoothing factor (`smoothing = 0.2`) controls cursor responsiveness — closer to `1.0` is more responsive but jittery, closer to `0.0` is smoother but sluggish.

## Use Cases

This project demonstrates how a simple webcam and hand tracking can replace physical input devices entirely. Below are real-world scenarios where this technology can be applied:

| Scenario | Description |
|---|---|
| **Touchless Shopping** | Browse an online store, add items to cart, and complete a purchase — all without touching a mouse or keyboard. Ideal for kiosk environments or hygiene-sensitive settings. |
| **Card & Board Games** | Play digital card games or board games using only hand gestures in front of a camera. Pinch to pick up cards, drag to place them, tap gestures to click. |
| **Accessibility** | Enables people with limited hand mobility or motor disabilities to control a computer with minimal physical effort. |
| **Presentation Control** | Advance slides, click links, and interact with presentation software during a talk — hands-free and without a clicker. |
| **Smart TV / Kiosk UI** | Control a media interface or information kiosk from a distance without touching the screen — useful in public spaces. |
| **Sterile Environments** | Surgeons or lab technicians can interact with software (e.g., viewing scans) without breaking sterile protocol. |
| **Interactive Installations** | Museums, exhibitions, and retail displays can offer gesture-driven interactive experiences to visitors. |

## Tech Stack

- [OpenCV](https://opencv.org/) — webcam capture and display
- [MediaPipe](https://mediapipe.dev/) — real-time hand landmark detection
- [PyAutoGUI](https://pyautogui.readthedocs.io/) — cross-platform mouse control
- [NumPy](https://numpy.org/) — vector math for landmark distances and smoothing
