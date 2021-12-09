from window import MainWindow
from tkinter import *
from datetime import date
import os
import docx
import comtypes.client
import subprocess
from tkinter import filedialog


class CoverLetterWindow(MainWindow):
    def __init__(self):
        MainWindow.__init__(self)
        
        self._assignUI()
        self._packUI()
        self._windowLoop()
    
    def _assignUI(self):
        self._nameLbl = Label(self._window, text="Your Name:")
        self._companyNameLbl = Label(self._window, text="Enter Company Name:")
        self._companyNameEnt = Entry(self._window)
        self._positionLbl = Label(self._window, text="Position:")
        self._positionEnt = Entry(self._window)
        self._submitBtn = Button(self._window, text="Submit", command=self._processSubmit)
        self._spacerLbl = Label(self._window)
        self._openBtn = Button(self._window, text="Open Folder", command=self._openFolder)
        self._renameBtn = Button(self._window, text="Change Name", command=self._changeName)
    
    def _packUI(self):
        self._companyNameLbl.pack()
        self._companyNameEnt.pack()
        self._positionLbl.pack()
        self._positionEnt.pack()
        self._spacerLbl.pack()
        self._submitBtn.pack()
        self._openBtn.pack()
        self._renameBtn.pack()
    
    def _unpackUI(self):
        self._companyNameLbl.pack_forget()
        self._companyNameEnt.pack_forget()
        self._positionLbl.pack_forget()
        self._positionEnt.pack_forget()
        self._spacerLbl.pack_forget()
        self._submitBtn.pack_forget()
        self._openBtn.pack_forget()
        self._renameBtn.pack_forget()
    def _processSubmit(self):
        position = self._positionEnt.get()
        company = self._companyNameEnt.get()
        
        if position != "" and company != "":
            _CoverLetterGen(position, company)
            self._reload()
            
    def _openFolder(self):
        
        coverLetterDirectory = os.path.join(os.getcwd(), "Cover Letters")
        command = 'explorer.exe ' + coverLetterDirectory
        
        os.system(command)

        
        
        
        
        
        
        
    def _changeName(self):
        self._unpackUI()
        from namewindow import NameWindow
        NameWindow(True)
    
    def _reload(self):
        self._unpackUI()
        self.__init__()
     
class _GetDate():
    def __init__(self):
        self._dateAssign = date.today()
        self._today = self._dateAssign.strftime("%B %d, %Y")
        self._todayFolderFormat = self._dateAssign.strftime("%Y-%m-%d")
        
class _CoverLetterGen():
    def __init__(self, position, company):
        self._directory = os.getcwd()
        self._date = _GetDate()
        self._position = position
        self._company = company
        self._templateInserts = {"DATE":"", "POSITION":"", "COMPANY":"", "YOURNAME":""}
        self._templateDoc = docx.Document("template.docx")
        self._coverLetterDirectory = os.path.join(self._directory, "Cover Letters")
        self._coverLetterDatedDirectory = os.path.join(self._coverLetterDirectory, self._date._todayFolderFormat)
        self._createLetter()

        
    def _createLetter(self):
        self._getYourName()
        self._setTemplate()
        self._setFileName()
        self._replaceWords()
        self._setupDirectory()
        self._makePDF()

    
    def _getYourName(self):
        filename = os.path.join(self._directory, "name.txt")
        with open(filename, "r") as f:
            contents = f.read()
        self._yourName = contents
    
    def _setTemplate(self):
        self._templateInserts["DATE"] = self._date._today
        self._templateInserts["POSITION"] = self._position
        self._templateInserts["COMPANY"] = self._company
        self._templateInserts["YOURNAME"] = self._yourName
    
    def _setFileName(self):
        tempFileName = self._templateInserts["YOURNAME"] + " " + self._templateInserts["COMPANY"] + " " + self._templateInserts["POSITION"] + ".pdf"
        self._coverLetterFileName = tempFileName.replace(" ", "-")        
        
    def _replaceWords(self):
        for i in self._templateInserts:
            for t in self._templateDoc.paragraphs:
                if t.text.find(i) >= 0:
                    t.text = t.text.replace(i, self._templateInserts[i])
        self._templateDoc.save("temporaryTemplate.docx")
    
    def _setupDirectory(self):
        try:
            os.mkdir(self._coverLetterDirectory)
        except FileExistsError:
            pass
        try:
            os.mkdir(self._coverLetterDatedDirectory)
        except FileExistsError:
            pass
        
    def _makePDF(self):
        wdFormatPDF = 17
        tempFile = os.path.join(self._directory, "temporaryTemplate.docx")
        pdfFile = os.path.join(self._coverLetterDatedDirectory, self._coverLetterFileName)           
        word = comtypes.client.CreateObject('Word.Application')
        tempDoc = word.Documents.Open(tempFile)
        
        tempDoc.SaveAs(pdfFile, FileFormat=wdFormatPDF)
        tempDoc.Close()
        os.remove(tempFile)
        word.Quit()
        
if __name__ == '__main__':
    CoverLetterWindow()