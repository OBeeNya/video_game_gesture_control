from controller_overlay import ControllerOverlayApp
import customtkinter as ctk
import cv2
from gesture_control import GestureControl

class App(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.geometry('810x1080')
        self.title("Gesture Recognition")
        self.app1_frame = GestureControl(self)
        self.app1_frame.pack(side="top")
        self.app2_frame = ControllerOverlayApp(self)
        self.app2_frame.pack(side="bottom")
    
    def on_closing(self):
        self.app1_frame.recognizer.close()
        self.app1_frame.cap.release()
        cv2.destroyAllWindows()
        self.app2_frame.running = False
        self.app2_frame.pygame_thread.join()

if __name__ == '__main__':
    
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")
    app = App()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
