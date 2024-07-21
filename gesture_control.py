from imports import *

input_queue = queue.Queue()

class GestureControl(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(parent)
        self.pack(expand=True, fill="both")
        self.configure(fg_color='#ccccff')

        self.gamepad = vg.VDS4Gamepad()
        self.keys = {
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

        self.cap = cv2.VideoCapture(0)
        self.image = None
        self.mp_hands = mp.solutions.hands
        self.results = []
        self.recognizer = None

        self.video_label = ctk.CTkLabel(self, text="")
        self.video_label.pack(expand=True, fill="both")

        self.video_thread = threading.Thread(target=self.start_video, daemon=True)
        self.video_thread.start()

    def __save_result(self, result: vision.GestureRecognizerResult,
                    unused_output_image: mp.Image, timestamp_ms: int):
        self.results.append(result)

    def __process_gesture(self, hand, gesture):

        if gesture in self.keys[hand].keys():

            input_queue.put(hand+' '+gesture)
         
            self.gamepad.press_button(button=self.keys[hand][gesture])
            self.gamepad.update()
            time.sleep(0.5)
         
            self.gamepad.release_button(button=self.keys[hand][gesture])
            self.gamepad.update()
            time.sleep(0.5)

    def __process_left_joystick(self, hand_landmarks):

        index = hand_landmarks[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
        self.gamepad.left_joystick(
            x_value=int(-index.x*255+255),
            y_value=int(index.y*255))
        time.sleep(0.05)
        self.gamepad.update()

    def start_video(self):

        model_asset_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'tasks',
            'gesture_recognizer.task')
        base_options = python.BaseOptions(model_asset_path=model_asset_path)
        options = vision.GestureRecognizerOptions(base_options=base_options,
            running_mode=vision.RunningMode.LIVE_STREAM,
            num_hands=2,
            result_callback=self.__save_result)
        self.recognizer = vision.GestureRecognizer.create_from_options(options)
    
        while self.cap.isOpened():
        
            _, image = self.cap.read()
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_image)

            self.recognizer.recognize_async(mp_image, time.time_ns() // 1_000_000)

            if self.results:

                for (hand_index, hand_landmarks), hand in zip(
                    enumerate(self.results[0].hand_landmarks), self.results[0].handedness):

                    hand = hand[0].display_name

                    if self.results[0].gestures:
                        gesture = self.results[0].gestures[hand_index][0].category_name
                        if gesture != 'None':
                            self.__process_gesture(hand, gesture)
                        if hand == 'Left' and gesture not in self.keys['Left'].keys():
                            self.__process_left_joystick(hand_landmarks)

                self.results.clear()

            img = Image.fromarray(rgb_image)
            imgtk = ImageTk.PhotoImage(image=img)
            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk)
            time.sleep(0.03)

        self.recognizer.close()
        self.cap.release()
        cv2.destroyAllWindows()
