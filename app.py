from controller_overlay import ControllerOverlay
from gesture_control import GestureControl
from imports import *

class App(ctk.CTk):

    def __init__(self):

        super().__init__()
        self.geometry('810x1080')
        self.title("Gesture Recognition")
        
        icon_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'assets',
            'app_icon.ico')
        self.iconbitmap(icon_path)
        
        self.app1_frame = GestureControl(self)
        self.app2_frame = ControllerOverlay(self)

if __name__ == '__main__':
    
    app = App()
    app.mainloop()
