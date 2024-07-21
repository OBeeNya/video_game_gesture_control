from gesture_control import input_queue
from imports import *
import gamepad_assets

class ControllerOverlay(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(parent)
        self.parent = parent
        self.pack(expand=True, fill="both")

        self.asset_map = gamepad_assets.PS4Assets()
        self.asset_map.load()
        self.running = False
        self.window_is_framed = True
        self.trigger_deadzone = 0.002

        pygame.joystick.init()
        self.controller = pygame.joystick.Joystick(0)
        self.controller.init()
        self.BUTTON_TRANSLATION = gamepad_assets.buttons

        pygame.init()
        size = self.asset_map._base.get_size()
        self.window_size = (size[0] + 10, size[1] + 10)
        self.screen = pygame.Surface(self.window_size)
        self.screen.fill((204, 204, 255))
        pygame.display.set_caption('Controller Visualisation Overlay')

        self.image_label = ctk.CTkLabel(self, text='')
        self.image_label.pack(expand=True, fill="both")
        self.update_image()

        self.pygame_thread = threading.Thread(target=self.run_pygame, daemon=True)
        self.pygame_thread.start()

    def run_pygame(self):

        self.running = True
        while self.running:
            self.image_label.configure(text=input_queue.get())
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.blit(self.asset_map._base, (5, 5))

            for button_num in range(self.controller.get_numbuttons()):
                button_is_pressed = self.controller.get_button(button_num)
                try:
                   button_ID = self.BUTTON_TRANSLATION[button_num]
                except:
                    button_ID = None
                if button_ID in self.asset_map.analogs and not button_is_pressed:
                    if button_ID == self.asset_map.left_analog:
                        left_analog = self.asset_map[button_ID][button_is_pressed]
                    else:
                        right_analog = self.asset_map[button_ID][button_is_pressed]
                elif button_ID in self.asset_map.analogs and button_is_pressed:
                    if button_ID == self.asset_map.left_analog:
                        left_analog = self.asset_map[button_ID][button_is_pressed]
                    else:
                        right_analog = self.asset_map[button_ID][button_is_pressed]
                elif button_ID not in self.asset_map.analogs:
                    try:
                        btndat = self.asset_map[button_ID][button_is_pressed]
                        self.screen.blit(btndat['img'], btndat['loc'])
                    except (KeyError, TypeError):
                        continue

            left_ana_horiz = round(self.controller.get_axis(self.BUTTON_TRANSLATION[self.asset_map.left_stick_x]), 2)
            left_ana_verti = round(self.controller.get_axis(self.BUTTON_TRANSLATION[self.asset_map.left_stick_y]), 2)
            right_ana_horiz = round(self.controller.get_axis(self.BUTTON_TRANSLATION[self.asset_map.right_stick_x]), 2)
            right_ana_verti = round(self.controller.get_axis(self.BUTTON_TRANSLATION[self.asset_map.right_stick_y]), 2)

            self.screen.blit(left_analog['img'], (left_analog['loc'][0] + (30 * left_ana_horiz), left_analog['loc'][1] + (30 * left_ana_verti)))
            self.screen.blit(right_analog['img'], (right_analog['loc'][0] + (30 * right_ana_horiz), right_analog['loc'][1] + (30 * right_ana_verti)))

            lt = self.asset_map.left_trigger
            rt = self.asset_map.right_trigger
            if max(0, (self.controller.get_axis(5) + 1) / 2) > self.trigger_deadzone:
                self.screen.blit(lt['img'], lt['loc'])
            if max(0, (self.controller.get_axis(4) + 1) / 2) > self.trigger_deadzone:
                self.screen.blit(rt['img'], rt['loc'])

            self.update_image()
            pygame.time.delay(30)

        pygame.quit()

    def update_image(self):

        pygame_image = pygame.surfarray.array3d(self.screen)
        pygame_image = pygame_image.swapaxes(0, 1)
        pil_image = Image.fromarray(pygame_image)
        imgtk = ImageTk.PhotoImage(pil_image)
        self.image_label.imgtk = imgtk
        self.image_label.configure(image=imgtk)
