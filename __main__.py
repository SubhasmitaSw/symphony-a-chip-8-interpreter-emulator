import tkinter
from window import Window
from interpreter import Interpreter
from renderer import Renderer
from file_io import FileIO
from keymap import Keymap
from audio import AudioSynthesizer

copyright_frame = None

def show_copyright(root, width, height):
    copyright_frame = tkinter.Toplevel(root, width=width, height=height)
    copyright_frame.title("Copyright Info")
    label = tkinter.Label(copyright_frame, text="Copyright 2020, Chris Bell", fg="red")
    label.pack();
    copyright_frame.protocol("WM_DELETE_WINDOW", copyright_frame.destroy)

def main():

    root = tkinter.Tk()
    root.resizable(False, False)

    # OpenGL display
    display = Renderer()

    # Keymap/Input
    keymap = Keymap(root)
    root.bind('<KeyPress>', keymap.process_keypress)
    root.bind('<KeyRelease>', keymap.process_keyrelease)

    # Audio synthesizer
    audio = AudioSynthesizer()

    # Chip-8 interpreter
    interpreter = Interpreter(display, keymap, audio)

    # File manager
    file_io = FileIO(interpreter)

    # Setup the main window frame
    window = Window(root, display, interpreter, file_io, keymap, audio, width=720, height=480)
    # Approximate milliseconds between update calls
    window.animate = int(1000 / display.max_fps)
    window.pack(fill=tkinter.BOTH, expand=False)

    # Menu bar
    menu_bar = tkinter.Menu(root)
    file_menu = tkinter.Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="Open ROM...", command=file_io.open)
    file_menu.add_command(label="Save state...", command=file_io.save_state)
    file_menu.add_command(label="Load state...", command=file_io.load_state)
    file_menu.add_command(label="Keyboard settings...", command=keymap.open_window)
    file_menu.add_command(label="About...", command=lambda: show_copyright(root, 720, 480))

    file_menu.add_separator()

    file_menu.add_command(label="Quit", command=window.close)
    menu_bar.add_cascade(label="File", menu=file_menu)

    root.config(menu=menu_bar)

    root.protocol("WM_DELETE_WINDOW", window.close)

    if interpreter.debug:
        # Show GPU info
        window.after(100, window.printContext)

    window.mainloop()


if __name__ == '__main__':
    main()