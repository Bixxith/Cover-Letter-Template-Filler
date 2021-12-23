from tkinter import *
import re

from window import MainWindow
from templateframe import TemplateFrame
from optionsframe import OptionsFrame
from variablesframe import VariablesFrame


class CoverLetterWindow(MainWindow):
    
    def __init__(self):
        MainWindow.__init__(self)
        self.templateFrame = TemplateFrame()
        self.optionsFrame = OptionsFrame()
        self.variablesFrame = VariablesFrame()
        self.assignUI()
        self.packUI()
        self.variablesFrame.verifyDirectory()
        self.templateFrame.autoLoad()
        self.getHeaderText()
        self.windowLoop()

    def assignUI(self):
        btnGeneratePDF = self.optionsFrame.btnGeneratePDF
        btnSave = self.optionsFrame.btnSave
        btnLoad = self.optionsFrame.btnLoad
        btnSave.configure(command=self.templateFrame.manualSave)
        btnLoad.configure(command=self.templateFrame.manualLoad)
        btnGeneratePDF.configure(command=self.generateLetter)
  
    def getHeaderText(self):
        self.optionsFrame.headerText = self.variablesFrame.getHeaderText()
        
    def getText(self):
        return self.templateFrame.getText()
           
    def replaceKeywords(self):
        keywordDict= {'COMPANY':(self.getCompany(), "COMPANY"),
                      'DATE':(self.getDate(), "DATE"),
                      'YOURNAME':(self.getName(), "YOURNAME"),
                      'POSITION':(self.getPosition(), "POSITION")}
        rawText = self.getText()
        textField = ' '.join(rawText)
        for items in keywordDict.values():
            textField = re.sub(items[1], items[0], textField)
        return(textField)

    def packUI(self):
        self.optionsFrame.packUI()
        self.templateFrame.packUI()
        self.variablesFrame.packUI()
        self.mainFrame.pack(anchor=CENTER)
        
    def generateLetter(self):
        template = self.replaceKeywords()
        self.optionsFrame.generateLetter(template, self.getName(), 
                                         self.getCompany(),self.getPosition())
    
    def getDate(self):
        return self.variablesFrame.getDate()
    
    def getName(self):
        return self.variablesFrame.getName() 
    
    def getPosition(self):
        return self.variablesFrame.getPosition()
    
    def getCompany(self):
        return self.variablesFrame.getCompany()     
     
if __name__ == '__main__':
    CoverLetterWindow()