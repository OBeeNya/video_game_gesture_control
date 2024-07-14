import cv2
import mediapipe as mp
import os
import time
import vgamepad as vg

model_path = os.path.join(os.getcwd(), 'models', 'gesture_recognizer.task')

BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

options = GestureRecognizerOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=VisionRunningMode.VIDEO)

recognizer = GestureRecognizer.create_from_options(options)

gamepad = vg.VDS4Gamepad()
key_mapping = {
    'Closed_Fist': vg.DS4_BUTTONS.DS4_BUTTON_CIRCLE,
    'Open_Palm': vg.DS4_BUTTONS.DS4_BUTTON_SHOULDER_RIGHT,
    # 'Pointing_Up': None,
    # 'Thumb_Down': None,
    'Thumb_Up': vg.DS4_BUTTONS.DS4_BUTTON_SQUARE,
    'Victory': vg.DS4_BUTTONS.DS4_BUTTON_TRIANGLE,
    'ILoveYou': vg.DS4_BUTTONS.DS4_BUTTON_CROSS,
}

running = True
cap = cv2.VideoCapture(0)

previous = None
while running:
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
    gesture_recognition_result = recognizer.recognize_for_video(mp_image, int(time.time() * 1000))
    if gesture_recognition_result.gestures and gesture_recognition_result.gestures[0][0].category_name in key_mapping.keys():
        category = gesture_recognition_result.gestures[0][0].category_name
        gamepad.press_button(button=key_mapping[category])
        gamepad.update()
        time.sleep(1.0)
        gamepad.release_button(button=key_mapping[category])
        gamepad.update()
