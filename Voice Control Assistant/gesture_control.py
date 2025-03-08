import cv2
import mediapipe as mp
import pyautogui
import time

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, 
                       min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Get screen size
screen_width, screen_height = pyautogui.size()

# Open webcam
cap = cv2.VideoCapture(0)

# To avoid spam clicking, add a cooldown
last_click_time = time.time()

print("Gesture-based mouse control started. Press 'q' to exit.")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    frame_height, frame_width, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get finger tip coordinates
            index_tip = hand_landmarks.landmark[8]
            thumb_tip = hand_landmarks.landmark[4]

            # Map index finger position to screen coordinates (cursor movement)
            screen_x = int(index_tip.x * screen_width)
            screen_y = int(index_tip.y * screen_height)

            # Move mouse cursor
            pyautogui.moveTo(screen_x, screen_y)

            # Calculate pinch distance (thumb tip & index tip)
            distance = ((thumb_tip.x - index_tip.x)**2 + (thumb_tip.y - index_tip.y)**2)**0.5

            # Click if pinch detected and cooldown passed
            if distance < 0.03 and time.time() - last_click_time > 0.5:  # Adjust distance if needed
                pyautogui.click()
                last_click_time = time.time()

            # Display finger position & click prompt
            cv2.putText(frame, f"Mouse: {screen_x}, {screen_y}", (50, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            if distance < 0.03:
                cv2.putText(frame, "Click!", (screen_x, screen_y - 20), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow("Gesture Control Mouse", frame)

    # Exit on 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
