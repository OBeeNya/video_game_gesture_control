import asyncio
import cv2
import mediapipe as mp
import os
import time
import vgamepad as vg

class GestureControl:

    def __init__(self):

        self.gamepad = vg.VDS4Gamepad()
        self.keys = {
            'Right': {
                'Closed_Fist': vg.DS4_BUTTONS.DS4_BUTTON_CIRCLE,
                'Open_Palm': vg.DS4_BUTTONS.DS4_BUTTON_SHOULDER_RIGHT,
                'Pointing_Up': vg.DS4_BUTTONS.DS4_BUTTON_THUMB_LEFT,
                'Thumb_Down': vg.DS4_BUTTONS.DS4_BUTTON_SHARE,
                'Thumb_Up': vg.DS4_BUTTONS.DS4_BUTTON_SQUARE,
                'Victory': vg.DS4_BUTTONS.DS4_BUTTON_TRIANGLE,
                'ILoveYou': vg.DS4_BUTTONS.DS4_BUTTON_CROSS},
            'Left': {
                'Closed_Fist': vg.DS4_BUTTONS.DS4_BUTTON_SHOULDER_LEFT,
                'Open_Palm': vg.DS4_BUTTONS.DS4_BUTTON_TRIGGER_LEFT}}
        self.previous = {
            'Left': None,
            'Right': None}

        model_asset_path = str(os.path.join(os.getcwd(),'tasks','gesture_recognizer.task'))
        base_options = mp.tasks.BaseOptions(model_asset_path=model_asset_path)
        options = mp.tasks.vision.GestureRecognizerOptions(
            base_options=base_options,
            running_mode=mp.tasks.vision.RunningMode.VIDEO)
        self.recognizer = mp.tasks.vision.GestureRecognizer.create_from_options(options)

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)

        self.watching = True

    async def handle_left_joystick(self, frame, hand_landmarks):

        index_finger_landmarks = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]

        # index_finger_x = int(index_finger_landmarks.x * frame.shape[1])
        # index_finger_y = int(index_finger_landmarks.y * frame.shape[0])

        # x_value_float = 1 if ((4 * index_finger_x / frame.shape[1]) - 1) > 1 else (4 * index_finger_x / frame.shape[1]) - 1
        # y_value_float = (2 * index_finger_y / frame.shape[0]) - 1
        x_value_float = index_finger_landmarks.x * 2 - 1
        y_value_float = index_finger_landmarks.y * 2 - 1

        self.gamepad.left_joystick_float(x_value_float=x_value_float, y_value_float=y_value_float)
        self.gamepad.update()

    def process_hand(self, frame, hand, hand_landmarks):
    # async def process_hand(self, frame, hand, hand_landmarks):

        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        gesture_recognition_result = self.recognizer.recognize_for_video(mp_image, int(time.time() * 1000))

        if gesture_recognition_result.gestures and gesture_recognition_result.gestures[0][0].category_name in self.keys[hand].keys():

            category = gesture_recognition_result.gestures[0][0].category_name
            print(hand, category)

            # if self.previous[hand] and self.previous[hand] != category:
            #     self.gamepad.release_button(button=self.keys[hand][self.previous[hand]])
            #     self.gamepad.update()
            #     time.sleep(0.1)

            self.gamepad.press_button(button=self.keys[hand][category])
            self.gamepad.update()
            time.sleep(1)
            self.gamepad.release_button(button=self.keys[hand][category])
            self.gamepad.update()
            time.sleep(1)

            self.previous[hand] = category

        # if hand == 'Left':
        #     await self.handle_left_joystick(frame, hand_landmarks)

    def private_watch(self):
    # async def private_watch(self):

        cap = cv2.VideoCapture(0)

        while self.watching:

            _, frame = cap.read()
            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            hand_results = self.hands.process(rgb_frame)

            if hand_results.multi_hand_landmarks:
                # tasks = []
                for hand_landmarks, handedness in zip(hand_results.multi_hand_landmarks, hand_results.multi_handedness):
                    hand = handedness.classification[0].label
                    self.process_hand(frame, hand, hand_landmarks)
                    # task = asyncio.create_task(self.process_hand(frame, hand, hand_landmarks))
                #     tasks.append(task)
                # await asyncio.gather(*tasks)

    def watch(self):

        self.private_watch()
        # asyncio.run(self.private_watch())

instance = GestureControl()
instance.watch()
