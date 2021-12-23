from tkinter import Text, Frame, IntVar
from tkinter.constants import LEFT, TOP, Y, END
import tkinter.font as tkFont
from os.path import exists

from window import MainWindow

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
        self.templateDictionary = {'DATE':'', 'COMPANY':'', 
                                   'POSITION':'', 'YOURNAME':''}
        self.highlightKeywords()
    def assignUI(self):
        self.frame = Frame(self.mainFrame, height=1000, width=1000)
        self.templateTextArea = Text(self.frame, height = 50, width = 100, 
                                     font=fontCal, pady=20, undo=True, 
                                     autoseparators=True, maxundo=-1, 
                                     highlightbackground='black', 
                                     highlightthickness=1)
        
        self.templateTextArea.bind('<Key>', self.highlightKeywordsClicked)
        self.templateTextArea.bind('<FocusOut>', self.autoSave)
         
    def packUI(self):
        self.templateTextArea.pack(side=TOP, pady=10)
        self.frame.pack_propagate(0)
        self.frame.pack(side = LEFT, expand=False, fill=Y)
    
    def highlightKeywordsClicked(self,event):
        self.highlightKeywords()
        
    def highlightKeywords(self):
        for items in self.templateDictionary:
            self.highlightKeywordsTagger(items)
            
    def highlightKeywordsTagger(self, pattern, start="1.0",end="end"):
        textBox = self.templateTextArea
        start = textBox.index(start)
        end = textBox.index(end)
        textBox.mark_set("matchStart", start)
        textBox.mark_set("matchEnd", start)
        textBox.mark_set("searchLimit", end)
        textBox.tag_configure("yellow", background="#FFFF00")
        count = IntVar()
        while True:
            index = textBox.search(pattern, "matchEnd",
                                "searchLimit", count=count, 
                                regexp=True)
            if index == "": break
            if count.get() == 0: break
            textBox.mark_set("matchStart", index)
            textBox.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
            textBox.tag_add("yellow", "matchStart", "matchEnd")
        
    def getText(self):
        text = self.templateTextArea.get("1.0", END)
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