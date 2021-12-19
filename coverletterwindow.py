from window import MainWindow
from templateframe import TemplateFrame
from optionsframe import OptionsFrame
from variablesframe import VariablesFrame
from tkinter import *


class CoverLetterWindow(MainWindow):
    
    def __init__(self):
        MainWindow.__init__(self)
        self.templateFrame = TemplateFrame()
        self.optionsFrame = OptionsFrame()
        self.variablesFrame = VariablesFrame()

        self.assignUI()
        self.packUI()
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
        keywordDict= {'COMPANY':self.getCompany(),'DATE':self.getDate(), 'YOURNAME':self.getName(),'POSITION':self.getPosition()}
        textField = self.getText()
        
        for each in keywordDict:
            
            # preserves the text surrounding the keyword in case it has new lines around it
            slicedWord = slice(0, len(each))
            otherHalf = slice(len(each), len(each) + len(each))
            
            # checks to see if string is an exact match, then checks to see if string contains the keyword and replaces it accordingly
            for i in range(len(textField)):
                if textField[i][slicedWord] == each:
                    textField[i] = keywordDict[each] + textField[i][otherHalf]
                elif each in textField[i]:
                    index = textField[i].find(each)
                    firstHalf = slice(0, index)
                    secondHalf = slice(index+len(each), len(textField[i]))
                    newString = textField[i][firstHalf] + keywordDict[each] + textField[i][secondHalf]
                    textField[i] = newString                   
        return ' '.join(textField)
        
        
    def packUI(self):
        self.optionsFrame.packUI()
        self.templateFrame.packUI()
        self.variablesFrame.packUI()
        self.mainFrame.pack(anchor=CENTER)
        
        
    def generateLetter(self):
        template = self.replaceKeywords()
        self.optionsFrame.generateLetter(template, self.getName(), self.getCompany(),self.getPosition())
        
    
    def getDate(self):
        return self.variablesFrame.getDate()
    
    
    def getName(self):
        return self.variablesFrame.getName() 
    
    
    def getPosition(self):
        return self.variablesFrame.getPosition()
    
    
    def getCompany(self):
        return self.variablesFrame.getCompany()     
    
    
    def _changeName(self):
        self._unpackUI()
        from variablesframe import NameWindow
        NameWindow(True)
    
    
    def reload(self):
        self._unpackUI()
        self.__init__()
     
     
     
if __name__ == '__main__':
    CoverLetterWindow()