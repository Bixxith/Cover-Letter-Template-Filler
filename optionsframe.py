from tkinter.constants import LEFT, BOTH, W, TOP
from tkinter import Frame, Button, messagebox
from datetime import date
import os
from os.path import exists

from fpdf import FPDF

from window import MainWindow


class OptionsFrame(MainWindow):
    
    def __init__(self):
        MainWindow.__init__(self)
        self.createFrame()
        self.assignUI()
        self.datedDirectory()
        self.headerText = ''
        
    def datedDirectory(self):
        dateAssign = date.today()
        todayFolderFormat = dateAssign.strftime("%Y-%m-%d")
        self.coverLetterDirectory = os.path.join(os.getcwd(), "Cover Letters")
        self.coverLetterDatedDirectory = os.path.join(self.coverLetterDirectory, 
                                                      todayFolderFormat)
        
    def createFrame(self):
        self.frame = Frame(self.mainFrame, width=100, height=100)
            
    def assignUI(self):
        self.pdfFrame = Frame(self.frame, height=100)
        self.btnOpen = Button(self.pdfFrame, text = "Open Folder", 
                              command = self.openFolder)
        self.btnGeneratePDF = Button(self.pdfFrame, text = "Generate PDF", 
                                     height=5, width=15)
        self.saveFrame = Frame(self.frame, height=100)
        self.btnSave = Button(self.saveFrame, text="Save Template")
        self.btnLoad = Button(self.saveFrame, text="Load Template")
    
    def packUI(self):
        self.pdfFrame.pack(side=TOP, pady=10, padx=10)
        self.saveFrame.pack(side=TOP, pady=10, padx=10)
        self.btnGeneratePDF.pack(pady=10)
        self.btnOpen.pack(padx=10, pady=10)  
        self.btnSave.pack(padx=10)
        self.btnLoad.pack(padx=10)
        self.frame.pack(anchor = W, side = LEFT, expand=True, fill=BOTH)
    
    def openFolder(self):
        command = 'explorer.exe '
        if os.path.isdir(self.coverLetterDatedDirectory):
            command += self.coverLetterDatedDirectory
        else:
            command += self.coverLetterDirectory
        os.system(command)
    
    def generateLetter(self, input, name, company, position):
        if len(input) > 2:
            if name: 
                if company and position:
                    pass
                else:
                    messagebox.showinfo("Company Information Missing",
                                        "Please list the company and position.")
                    return
            else:
                messagebox.showinfo("Name Missing",
                                    "Please set your name.")
                return
        else:
            messagebox.showinfo("Template Missing",
                                "Please create a template.")
            return
        pdf = FPDF()
        if os.path.isdir(self.coverLetterDatedDirectory):
            pdfdirectoryTemp = self.coverLetterDatedDirectory
        else:
            os.mkdir(self.coverLetterDatedDirectory)
            pdfdirectoryTemp = self.coverLetterDatedDirectory  
        pdfFileNameTemp = f'{name} {company} {position} Cover Letter.pdf'
        pdfFileName = pdfFileNameTemp.replace(' ', '-')
        pdfDirectory = os.path.join(pdfdirectoryTemp, pdfFileName)
        pdf.add_page()
        pdf.set_font('Helvetica', style='I', size=25)
        pdf.set_draw_color(r=0, g=158, b=255)
        pdf.set_line_width(width = .5)
        pdf.cell(0, h=15, txt=name, border = 'TB', ln = 2, align='C')
        pdf.set_font("Helvetica", size= 10)
        pdf.cell(0, h=10, txt=self.headerText, ln = 2, align="C")
        pdf.ln()
        pdf.set_font("Helvetica", size= 11)
        pdf.write(5, input)
        if exists(pdfDirectory):
            messagebox.showerror("PDF Exists",
                                 f'The cover letter for the {position}' +
                                 f'position at {company} already exists.')
        else:
            pdf.output(pdfDirectory)
            if exists(pdfDirectory):
                messagebox.showinfo("PDF Created", 
                                    f'The cover letter for the {position}' +
                                    f'position at {company} was created.')
            else:
                messagebox.showerror("PDF Creation Failed",
                                     "The cover letter was not created")
            