import customtkinter
import gesture_control
from PIL import Image, ImageTk

customtkinter.set_appearance_mode('dark')
customtkinter.set_default_color_theme('blue')

app = customtkinter.CTk()
app.geometry('400x240')

button = customtkinter.CTkButton(
    master=app,
    text='Launch Gesture Control',
    command=gesture_control.main) 
button.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)

if gesture_control.image != None:
    b,g,r = gesture_control.cv2.split(gesture_control.image)
    img = gesture_control.cv2.merge((r, g, b))
    im = Image.fromarray(img)
    imgtk = ImageTk.PhotoImage(image=im)
    customtkinter.CTkLabel(app, image=imgtk).pack()

if __name__ == '__main__':
    app.mainloop()
