from tkinter import *


class MainWindow():
    _window = Tk()
    def __init__(self):
        self._setupWindow()

    def _setupWindow(self):
        self._window.geometry("300x300")
        self._window.title("Cover Letter Template Filler")
        
        # Centers the window on the screen
        _windowWidth = self._window.winfo_reqwidth()
        _positionRight = int(self._window.winfo_screenwidth()/2 - _windowWidth/2)
        _windowHeight = self._window.winfo_reqheight()
        _positionDown = int(self._window.winfo_screenheight()/2 - _windowHeight/2)
        
        self._window.geometry("+{}+{}".format(_positionRight, _positionDown))
    
    def _windowLoop(self):
        self._window.mainloop()

if __name__ == "__main__":
    MainWindow()    
