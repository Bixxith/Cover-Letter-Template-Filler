import docx
import os
import comtypes.client
from tkinter import *
from datetime import date
import subprocess


class YourName():
    def __init__(self): 
        self.mainWindow = Tk()
        self.mainWindow.geometry("200x150")
        self.mainWindow.title("Cover Letter Generator Program")
        self.windowWidth = self.mainWindow.winfo_reqwidth()
        self.windowHeight = self.mainWindow.winfo_reqheight()
        self.positionRight = int(self.mainWindow.winfo_screenwidth()/2 - self.windowWidth/2)
        self.positionDown = int(self.mainWindow.winfo_screenheight()/2 - self.windowHeight/2)
        self.mainWindow.geometry("+{}+{}".format(self.positionRight, self.positionDown))
        
        self.invisLbl = Label(self.mainWindow)
        self.invisLbl2 = Label(self.mainWindow)
        self.nameLbl = Label(self.mainWindow, text="Enter your name: ")
        self.nameEntry = Entry(self.mainWindow)
        self.submitNameBtn = Button(self.mainWindow, text="Submit Name", command=self.submitName)
        self.directory = os.getcwd()


        self.invisLbl.pack()
        self.nameLbl.pack()
        self.nameEntry.pack()
        self.invisLbl2.pack()
        self.submitNameBtn.pack()
        
        self.mainWindow.mainloop()
        
    def submitName(self):
        filePath = os.path.join(self.directory, "name.txt")
        file = open(filePath, "w")
        file.write(self.nameEntry.get())
        file.close()
        self.mainWindow.destroy()
        CLGenerator()




class CLGenerator():
    def __init__(self):
        
        # Main Window Setup
        self.mainWindow = Tk()
        self.mainWindow.geometry("200x200")
        self.mainWindow.title("Cover Letter Generator Program")
        self.windowWidth = self.mainWindow.winfo_reqwidth()
        self.windowHeight = self.mainWindow.winfo_reqheight()
        self.positionRight = int(self.mainWindow.winfo_screenwidth()/2 - self.windowWidth/2)
        self.positionDown = int(self.mainWindow.winfo_screenheight()/2 - self.windowHeight/2)
        self.mainWindow.geometry("+{}+{}".format(self.positionRight, self.positionDown))
        
        # Variables
        self.dateAssign = date.today()
        self.today = self.dateAssign.strftime("%B %d, %Y")
        self.coverLetterFileName = ""
        self.directory = os.getcwd()
        self.cld1 = "Cover Letters"
        self.coverLetterDirectory = os.path.join(self.directory, self.cld1)
        self.cld2 = self.dateAssign.strftime("%Y-%m-%d")
        self.coverLetterDatedDirectory = os.path.join(self.coverLetterDirectory, self.cld2)
        self.yourName = ""
        self.templateInserts = {"DATE":"", "POSITION":"", "COMPANY":"", "YOURNAME":""}
        self.templateDoc = docx.Document("template.docx")

        
        # Tkinter widgets
        self.nameLbl = Label(self.mainWindow, text="Your Name:")
        self.companyNameLbl = Label(self.mainWindow, text="Enter Company Name:")
        self.companyNameEntry = Entry(self.mainWindow)
        self.positionLbl = Label(self.mainWindow, text="Position:")
        self.positionEntry = Entry(self.mainWindow)
        self.subBtn = Button(self.mainWindow, text="Submit", command=self.submit)
        self.invsLbl = Label(self.mainWindow)
        self.opnBtn1 = Button(self.mainWindow, text="Open Folder", command=self.openFolder)
        self.renameBtn = Button(self.mainWindow, text="Change Name", command=self.changeName)
        
        
        self.companyNameLbl.pack()
        self.companyNameEntry.pack()
        self.positionLbl.pack()
        self.positionEntry.pack()
        self.invsLbl.pack()
        self.subBtn.pack()
        self.opnBtn1.pack()
        self.renameBtn.pack()
        
        #Main loop
        self.mainWindow.mainloop()

    
    # Starts the Process
    def submit(self):
        if self.companyNameEntry.get() != "" and self.positionEntry.get() != "":
            self.compile()

    # Controls flow of process          
    def compile(self):
        self.getYourName()
        self.setTemplate()
        self.setFileName()
        self.replaceWords()
        self.setupDirectory()
        self.makePDF()
        self.reload()
    
    # Fills in the template dictionary values with gathered info
    def setTemplate(self):
        self.templateInserts["DATE"] = self.today
        self.templateInserts["POSITION"] = self.positionEntry.get()
        self.templateInserts["COMPANY"] = self.companyNameEntry.get()
        self.templateInserts["YOURNAME"] = self.yourName
        
    # Pulls the name from the text file
    def getYourName(self):
        fileName = os.path.join(self.directory, "name.txt")
        print(fileName)
        with open(fileName) as f:
            contents = f.read()
        self.yourName = contents
        
    # Generates the file name    
    def setFileName(self):
        preFileName = self.templateInserts["YOURNAME"] + " " + self.templateInserts["COMPANY"] + " " + self.templateInserts["POSITION"] + ".pdf"
        self.coverLetterFileName = preFileName.replace(" ", "-")

    # Replaces the words in the template
    def replaceWords(self):
        for i in self.templateInserts:
            for t in self.templateDoc.paragraphs:
                if t.text.find(i) >= 0:
                    t.text = t.text.replace(i, self.templateInserts[i])
        self.templateDoc.save("temporaryTemplate.docx")

    # Creates the directories for the Cover Letters
    def setupDirectory(self):
        try:
            os.mkdir(self.coverLetterDirectory)
                
        except FileExistsError:
            print("Cover Letter Folder exists, continuing.")
        try:
            os.mkdir(self.coverLetterDatedDirectory)
                
        except FileExistsError:
            print("Dated Folder exists, continuing.")
            
    # Creates the PDF and deletes the temporary file        
    def makePDF(self):
        wdFormatPDF = 17
        tempFile = os.path.join(self.directory, "temporaryTemplate.docx")
        pdfFile = os.path.join(self.coverLetterDatedDirectory, self.coverLetterFileName)
        word = comtypes.client.CreateObject('Word.Application')
        tempDoc = word.Documents.Open(tempFile)
        
        tempDoc.SaveAs(pdfFile, FileFormat=wdFormatPDF)
        tempDoc.Close()
        os.remove(tempFile)
        word.Quit()
    
    # Prompt to change name
    def changeName(self):
        YourName()
    
    # Clears the entry fields    
    def reload(self):
        self.mainWindow.destroy()
        CLGenerator()
    
    def openFolder(self):
        subprocess.Popen(r'explorer /select, %s' % self.coverLetterDatedDirectory)

        
# Checks to see if name.txt is set and starts accordingly
if __name__ == "__main__":    
    if not os.path.join(os.getcwd(), "name.txt"):
        YourName()
    else:
        CLGenerator()
