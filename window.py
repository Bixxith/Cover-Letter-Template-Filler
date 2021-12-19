from tkinter import Tk, Frame


class MainWindow():
    window = Tk()
    mainFrame = Frame(window)
    def __init__(self):
        self.setupWindow()
        


    def setupWindow(self):
        self.window.geometry("1400x1000")
        self.window.title("Cover Letter Template Filler")
        # self.window.resizable(False, False)
        # Centers the window on the screen
        # windowWidth = self.window.winfo_reqwidth()
        # positionRight = int(self.window.winfo_screenwidth()/2 - windowWidth/2)
        # windowHeight = self.window.winfo_reqheight()
        # positionDown = int(self.window.winfo_screenheight()/2 - windowHeight/2)
        
        # self.window.geometry("+{}+{}".format(positionRight, positionDown))
    
    def windowLoop(self):
        self.window.mainloop()

if __name__ == "__main__":
    MainWindow()    
