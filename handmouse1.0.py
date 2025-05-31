import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time

screen_w, screen_h = pyautogui.size()

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

prev_time = 0
last_click_time = 0

# Drag (basılı tutma) ve mouse hareket için
thumb_start_pos = None
mouse_start_pos = None
tracking_mouse = False

# Drag etkinliği kontrolü
dragging = False

# Smoothing için önceki mouse pozisyonu
prev_mouse_pos = np.array(pyautogui.position(), dtype=np.float64)
smoothing = 0.2

# Eşik değerleri (deneyerek ayarlayabilirsin)
THRESH_MOVE = 0.06
THRESH_DRAG = 0.06
THRESH_CLICK = 0.06

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        lm = results.multi_hand_landmarks[0].landmark

        # Landmark’lar
        thumb_tip = np.array([lm[4].x, lm[4].y])
        index_tip = np.array([lm[8].x, lm[8].y])
        middle_tip = np.array([lm[12].x, lm[12].y])
        ring_tip = np.array([lm[16].x, lm[16].y])

        # Mesafeler
        dist_thumb_index  = np.linalg.norm(thumb_tip - index_tip)
        dist_thumb_middle = np.linalg.norm(thumb_tip - middle_tip)
        dist_thumb_ring   = np.linalg.norm(thumb_tip - ring_tip)

        # --- Mouse hareket (thumb-index pinch) ---
        if dist_thumb_index < THRESH_MOVE:
            if not tracking_mouse:
                thumb_start_pos = thumb_tip.copy()
                mouse_start_pos = np.array(pyautogui.position())
                tracking_mouse = True
            else:
                delta = thumb_tip - thumb_start_pos
                move_x = delta[0] * screen_w * 2
                move_y = delta[1] * screen_h * 2

                target = mouse_start_pos + np.array([move_x, move_y])
                target[0] = np.clip(target[0], 0, screen_w - 1)
                target[1] = np.clip(target[1], 0, screen_h - 1)

                # Lerp smoothing
                prev_mouse_pos = prev_mouse_pos + (target - prev_mouse_pos) * smoothing
                pyautogui.moveTo(int(prev_mouse_pos[0]), int(prev_mouse_pos[1]))
        else:
            tracking_mouse = False

        # --- Drag (basılı tutma) (thumb-middle pinch) ---
        if dist_thumb_middle < THRESH_DRAG:
            if not dragging:
                pyautogui.mouseDown()
                dragging = True
        else:
            if dragging:
                pyautogui.mouseUp()
                dragging = False

        # --- Click (thumb-ring pinch) ---
        now = time.time()
        if dist_thumb_ring < THRESH_CLICK and (now - last_click_time) > 0.5:
            pyautogui.click()
            last_click_time = now

        mp_draw.draw_landmarks(frame, results.multi_hand_landmarks[0], mp_hands.HAND_CONNECTIONS)

    else:
        # Elleri göremezsek drag’i sonlandır
        if dragging:
            pyautogui.mouseUp()
            dragging = False
        tracking_mouse = False

    # FPS gösterimi
    curr_time = time.time()
    fps = 1 / (curr_time - prev_time) if prev_time else 0
    prev_time = curr_time
    cv2.putText(frame, f'FPS: {int(fps)}', (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Mouse Control", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
