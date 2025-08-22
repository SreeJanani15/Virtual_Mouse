import cv2
import mediapipe as mp
from controller import Controller

# Open webcam
camera = cv2.VideoCapture(0)

# Initialize Mediapipe Hands
mediapipe_hands = mp.solutions.hands
hand_tracker = mediapipe_hands.Hands()
drawing_utils = mp.solutions.drawing_utils

while True:
    # Capture video frame
    frame_captured, frame = camera.read()
    frame = cv2.flip(frame, 1)

    # Convert frame to RGB for Mediapipe
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    detection_results = hand_tracker.process(frame_rgb)

    if detection_results.multi_hand_landmarks:
        # Get first detected hand landmarks
        Controller.hand_landmarks = detection_results.multi_hand_landmarks[0]

        # Draw landmarks on frame
        drawing_utils.draw_landmarks(
            frame,
            Controller.hand_landmarks,
            mediapipe_hands.HAND_CONNECTIONS
        )

        # Perform gesture-based actions
        Controller.update_fingers_status()
        Controller.cursor_moving()
        Controller.detect_scrolling()
        Controller.detect_zooming()
        Controller.detect_clicking()
        Controller.detect_dragging()
        Controller.detect_minimize()
        Controller.detect_maximize()
        Controller.detect_close()

        # Exit gesture
        if Controller.detect_exit_gesture():
            break  

    # Show the frame
    cv2.imshow('Virtual Mouse', frame)

    # Exit on ESC key
    if cv2.waitKey(5) & 0xFF == 27:
        break
