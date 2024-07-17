import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import os
import time
import vgamepad as vg

gamepad = vg.VDS4Gamepad()
keys = {
    'Right': {
        'Closed_Fist': vg.DS4_BUTTONS.DS4_BUTTON_CIRCLE,
        'Open_Palm': vg.DS4_BUTTONS.DS4_BUTTON_SHOULDER_RIGHT,
        'Pointing_Up': vg.DS4_BUTTONS.DS4_BUTTON_THUMB_RIGHT,
        'Thumb_Down': vg.DS4_BUTTONS.DS4_BUTTON_SHARE,
        'Thumb_Up': vg.DS4_BUTTONS.DS4_BUTTON_SQUARE,
        'Victory': vg.DS4_BUTTONS.DS4_BUTTON_TRIANGLE,
        'ILoveYou': vg.DS4_BUTTONS.DS4_BUTTON_CROSS},
    'Left': {
        'Closed_Fist': vg.DS4_BUTTONS.DS4_BUTTON_SHOULDER_LEFT,
        'Open_Palm': vg.DS4_BUTTONS.DS4_BUTTON_TRIGGER_LEFT}}

mp_hands = mp.solutions.hands
cap = cv2.VideoCapture(0)
results = []
  
def save_result(result: vision.GestureRecognizerResult,
                unused_output_image: mp.Image, timestamp_ms: int):
    results.append(result)

def process_gesture(hand, gesture):
    if gesture in keys[hand].keys():
        print(hand, gesture)
        gamepad.press_button(button=keys[hand][gesture])
        gamepad.update()
        time.sleep(1.0)
        gamepad.release_button(button=keys[hand][gesture])
        gamepad.update()

def process_left_joystick(hand_landmarks):
    index = hand_landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    x_value_float = index.x * 2 - 1
    y_value_float = index.y * 2 - 1
    print(x_value_float, y_value_float)
    gamepad.left_joystick_float(
        x_value_float=x_value_float,
        y_value_float=y_value_float)
    gamepad.update()
    time.sleep(1.0)

def main():
  
    model_asset_path = str(os.path.join(
        os.getcwd(),
        'tasks',
        'gesture_recognizer.task'))
    base_options = python.BaseOptions(model_asset_path=model_asset_path)
    options = vision.GestureRecognizerOptions(base_options=base_options,
        running_mode=vision.RunningMode.LIVE_STREAM,
        num_hands=2,
        result_callback=save_result)
    recognizer = vision.GestureRecognizer.create_from_options(options)
  
    while cap.isOpened():
  
        _, image = cap.read()
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_image)
    
        recognizer.recognize_async(mp_image, time.time_ns() // 1_000_000)
    
        if results:
            for (hand_index, hand_landmarks), hand in zip(
                enumerate(results[0].hand_landmarks), results[0].handedness):

                hand = hand[0].display_name
                if results[0].gestures:
                    gesture = results[0].gestures[hand_index][0].category_name
                if gesture != 'None':
                    process_gesture(hand, gesture)
                elif hand == 'Left':
                    process_left_joystick(hand_landmarks)
    
            results.clear()
        
            cv2.imshow('Gesture Recognition', image)
    
        if cv2.waitKey(1) == 27:
            break
  
    recognizer.close()
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
