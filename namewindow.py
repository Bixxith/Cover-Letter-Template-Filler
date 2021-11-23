from window import MainWindow
from coverletterwindow import CoverLetterWindow
from tkinter import *
import os

class NameWindow(MainWindow):
    def __init__(self, change=False):
        MainWindow.__init__(self)
        self.changeName = change
        
        self._assignUI()
        self._packUI()
        self._windowLoop()
        
    def _assignUI(self):
        self._spacerLbl = Label(self._window)
        self._spacerLbl2 = Label(self._window)
        self._nameLbl = Label(self._window, text="Enter your name: ")
        self._nameEntry = Entry(self._window)
        self._submitNameBtn = Button(self._window, text="Submit Name", command=self._getNameEntry)

    def _packUI(self):
        self._spacerLbl.pack()
        self._nameLbl.pack()
        self._nameEntry.pack()
        self._spacerLbl2.pack()
        self._submitNameBtn.pack()
    
    def _unpackUI(self):
        self._spacerLbl.pack_forget()
        self._nameLbl.pack_forget()
        self._nameEntry.pack_forget()
        self._spacerLbl2.pack_forget()
        self._submitNameBtn.pack_forget()   
        
    def _getNameEntry(self):
        nameEntry = self._nameEntry.get()
        _GetName(nameEntry)
        self._unpackUI()
        CoverLetterWindow()

    
    
class _GetName():
    def __init__(self, nameEntry):
        self._name = nameEntry 
        
        self._makeFile()
        self._writeFile()
    
    def _makeFile(self):
        self._directory = os.getcwd()
        self._filePath = os.path.join(self._directory, "name.txt")
    
    def _writeFile(self):
        with open(self._filePath, "w") as file:
            file.write(self._name)                
                    

if __name__ == "__main__":
    NameWindow()