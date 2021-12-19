from tkinter import Text, Frame
from tkinter.constants import LEFT, TOP, Y, END
from window import MainWindow
import tkinter.font as tkFont
from os.path import exists

fontCal = tkFont.Font(name='Calibri')

initialTemplate = """DATE
COMPANY
RE: POSITION

To whom it may concern,

This is an example cover letter template.

Sincerely,
YOURNAME
"""


class TemplateFrame(MainWindow):
    def __init__(self):
        MainWindow.__init__(self)
        self.assignUI()
        self.templateDictionary = {'DATE':'', 'COMPANY':'', 'POSITION':'', 'YOURNAME':''}
        
        
    def assignUI(self):
        self.frame = Frame(self.mainFrame, height=1000, width=1000)
        self.templateTextArea = Text(self.frame, height = 50, width = 100, font=fontCal, pady=20, undo=True, autoseparators=True, maxundo=-1, highlightbackground='black', highlightthickness=1)
        
        self.templateTextArea.bind('<Key>', self.highlightKeywords)
        self.templateTextArea.bind('<FocusOut>', self.autoSave)
        
               
    def packUI(self):
        self.templateTextArea.pack(side=TOP, pady=10)
        self.frame.pack_propagate(0)
        self.frame.pack(side = LEFT, expand=False, fill=Y)
      
        
    def smallTextArea(self):
        self.templateTextArea.configure(height=50)
    
       
    def highlightKeywords(self, event):
        removeWhitespace = self.templateTextArea.get("1.0", END).replace('\n', ' ')
        textToHighlight = [word.strip(',.!?') for word in removeWhitespace.split(' ')]
        currentIndex = 1.0

        for i in range(len(textToHighlight)):
            if textToHighlight[i] in self.templateDictionary:
                word = textToHighlight[i]
                wordStart = self.templateTextArea.search(word, currentIndex, END)
                wordEnd = self.templateTextArea.search(' ', wordStart, END)
                
                self.templateTextArea.tag_add('highlight', wordStart, wordEnd )
                self.templateTextArea.tag_configure('highlight', background='yellow')
                self.templateTextArea.update()
                
                currentIndex = wordEnd
    
    
    def centerSelection(self):
       pass 
   
   
    def getText(self):
        text = self.templateTextArea.get("1.0", END) #.replace('\n', ' ')
        textField = [word for word in text.split(' ')]
        return textField
    
    
    def autoSave(self, event):
        text = ' '.join(self.getText())
        with open("Data/AutoSaveTemplate.txt", "w") as file:
            file.write(text)
    
    
    def autoLoad(self):
        self.templateTextArea.delete("1.0", "end")
        if exists("Data/AutoSaveTemplate.txt"):
            with open("Data/AutoSaveTemplate.txt") as file:
                self.templateTextArea.insert('1.0', file.read())
        else:
            self.templateTextArea.insert('1.0', initialTemplate)
              
                
    def manualSave(self):
        text = ' '.join(self.getText())
        with open("Data/Template.txt", "w") as file:
            file.write(text)
    
    
    def manualLoad(self):
        self.templateTextArea.delete("1.0", "end")
        with open("Data/Template.txt") as file:
            self.templateTextArea.insert('1.0', file.read())    
                
        





if __name__ == "__main__":
    TemplateFrame()        