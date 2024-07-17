from cx_Freeze import setup, Executable

setup(
    name="GestureControl",
    version="0.1",
    description="Control your video game using cam-recorded gestures.",
    executables=[Executable("gesture_control.py")],)
