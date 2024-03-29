
from tkinter import filedialog, messagebox
import ntpath


class FileIO:
    def __init__(self, interpreter):
        """Class for handling reading/writing to files"""
        self.interpreter = interpreter
        self.file_open = False
        self.rom = ''
        self.filename = ''
        return

    def open(self):
        self.filename = filedialog.askopenfilename(title='Choose your Game')
        # Strip file string from path string
        if not isinstance(self.filename, str):
            return
        self.rom = ntpath.basename(self.filename)
        # Open in binary mode
        try:
            with open(self.filename, 'rb') as file:
                self.interpreter.load_program_to_memory(file)
                self.file_open = True
        except IOError as error:
            if self.interpreter.debug:
                print(error)
            messagebox.showerror("ROM Error", "Couldn't open file")
            self.file_open = False

    def save_state(self):
        """Save the interpreter state"""
        return

    def load_state(self):
        """Load a saved interpreter state"""
        return