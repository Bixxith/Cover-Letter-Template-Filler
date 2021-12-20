from tkinter import Tk, Frame


class MainWindow():
    
    window = Tk()
    mainFrame = Frame(window)
    
    def __init__(self):
        self.setupWindow()
        
    def setupWindow(self):
        self.window.geometry("1400x1000")
        self.window.title("Cover Letter Template Filler")
  
    def windowLoop(self):
        self.window.mainloop()

if __name__ == "__main__":
    MainWindow()    
