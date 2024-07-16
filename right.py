import cv2
import mediapipe as mp
import os
import time
import vgamepad as vg

class GestureRight:

    def __init__(self):

        self.gamepad = vg.VDS4Gamepad()
        self.keys = {
            'Closed_Fist': vg.DS4_BUTTONS.DS4_BUTTON_CIRCLE,
            'Open_Palm': vg.DS4_BUTTONS.DS4_BUTTON_SHOULDER_RIGHT,
            'Pointing_Up': vg.DS4_BUTTONS.DS4_BUTTON_THUMB_LEFT,
            'Thumb_Down': vg.DS4_BUTTONS.DS4_BUTTON_SHARE,
            'Thumb_Up': vg.DS4_BUTTONS.DS4_BUTTON_SQUARE,
            'Victory': vg.DS4_BUTTONS.DS4_BUTTON_TRIANGLE,
            'ILoveYou': vg.DS4_BUTTONS.DS4_BUTTON_CROSS}

        model_asset_path = str(os.path.join(os.getcwd(),'tasks','gesture_recognizer.task'))
        base_options = mp.tasks.BaseOptions(model_asset_path=model_asset_path)
        options = mp.tasks.vision.GestureRecognizerOptions(
            base_options=base_options,
            running_mode=mp.tasks.vision.RunningMode.VIDEO)
        self.recognizer = mp.tasks.vision.GestureRecognizer.create_from_options(options)

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands()

        self.watching = True

    def handle_left_joystick(self, hand_landmarks):

        index_finger_landmarks = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
        x_value_float = index_finger_landmarks.x * 2 - 1
        y_value_float = index_finger_landmarks.y * 2 - 1

        self.gamepad.left_joystick_float(x_value_float=x_value_float, y_value_float=y_value_float)
        self.gamepad.update()

    def process_hand(self, frame, hand):

        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        gesture_recognition_result = self.recognizer.recognize_for_video(mp_image, int(time.time() * 1000))

        if gesture_recognition_result.gestures:
            print(hand, gesture_recognition_result.gestures[0][0].category_name)
        if gesture_recognition_result.gestures and gesture_recognition_result.gestures[0][0].category_name in self.keys.keys():

            category = gesture_recognition_result.gestures[0][0].category_name

            self.gamepad.press_button(button=self.keys[category])
            self.gamepad.update()
            time.sleep(1.0)
            self.gamepad.release_button(button=self.keys[category])
            self.gamepad.update()

    def private_watch(self):

        cap = cv2.VideoCapture(0)
        
        while self.watching:

            _, frame = cap.read()
            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            hand_results = self.hands.process(rgb_frame)

            if hand_results.multi_hand_landmarks:
                for handedness in  hand_results.multi_handedness:
                    hand = handedness.classification[0].label
                    # if hand == 'Right':
                    #     self.process_hand(frame)
                    self.process_hand(frame, hand)

    def watch(self):

        self.private_watch()

instance = GestureRight()
instance.watch()
