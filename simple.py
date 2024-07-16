import cv2
import mediapipe as mp
import os
import time

keys = {
    'Right': [
        'Closed_Fist',
        'Open_Palm',
        'Pointing_Up',
        'Thumb_Down',
        'Thumb_Up',
        'Victory',
        'ILoveYou'],
    'Left': [
        'Closed_Fist',
        'Open_Palm']}

model_asset_path = str(os.path.join(os.getcwd(),'tasks','gesture_recognizer.task'))
base_options = mp.tasks.BaseOptions(model_asset_path=model_asset_path)
options = mp.tasks.vision.GestureRecognizerOptions(
    base_options=base_options,
    num_hands=2,
    running_mode=mp.tasks.vision.RunningMode.VIDEO)

recognizer = mp.tasks.vision.GestureRecognizer.create_from_options(options)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

cap = cv2.VideoCapture(0)

while True:

    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    hand_results = hands.process(rgb_frame)
  
    if hand_results.multi_hand_landmarks:
  
        for hand_landmarks, handedness in zip(hand_results.multi_hand_landmarks, hand_results.multi_handedness):
  
            hand = handedness.classification[0].label
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
            gesture_recognition_result = recognizer.recognize_for_video(mp_image, int(time.time() * 1000))
  
            if gesture_recognition_result.gestures and gesture_recognition_result.gestures[0][0].category_name in keys[hand]:
                category = gesture_recognition_result.gestures[0][0].category_name
                print(hand, category)
