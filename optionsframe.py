from tkinter.constants import CENTER, DISABLED, FLAT, GROOVE, LEFT, BOTH, NORMAL, RAISED, RIDGE, RIGHT, SOLID, SUNKEN, W, TOP
from tkinter import READABLE, Frame, Button, StringVar, messagebox, Label, Checkbutton, Radiobutton, Entry, IntVar
import tkinter.font as tkFont
from datetime import date, timedelta, datetime
import os
from os.path import exists
import json
import sys
import shutil

from fpdf import FPDF

from window import MainWindow

fontHelv = ('Helvetica 10')
fontHelvTitle = ('Helvetica 13 underline')

class OptionsFrame(MainWindow):
    
    def __init__(self):
        MainWindow.__init__(self)
        self.createFrame()
        self.assignUI()
        self.datedDirectory()
        self.headerText = ''
        self.settings = dict()
        self.filePath = os.path.join(os.getcwd(), "Data/settings.json")
        self.loadOptions()
        self.runPurge()
        
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
                              command = self.openFolder,
                              bd=3, font=fontHelv)
        self.btnGeneratePDF = Button(self.pdfFrame, text = "Generate PDF", 
                                     height=5, width=15,
                                     bd=3, font=fontHelv)
        self.saveFrame = Frame(self.frame, height=100,
                                highlightbackground='black',
                                highlightthickness=1)
        self.btnSave = Button(self.saveFrame, text="Save", font=fontHelv, 
                              bd=3)
        self.btnLoad = Button(self.saveFrame, text="Load", font=fontHelv,
                              bd=3)
        self.lblTemplate = Label(self.saveFrame, text="Template", 
                            font=fontHelvTitle, )
        self.purgeFrame = Frame(self.pdfFrame, highlightbackground='black',
                                highlightthickness=1)
        self.lblPurge = Label(self.purgeFrame, 
                              text="Old Cover Letters",
                              font=fontHelvTitle)
        self.btnPurgeOld = Button(self.purgeFrame,
                                  text="Purge All",
                                  bd=3, font=fontHelv)
        self.autoPurgeFrame = Frame(self.purgeFrame)
        self.customPurgeFrame = Frame(self.autoPurgeFrame)
        self.rdoVariable = IntVar()
        self.chkVariable = IntVar()
        self.chkAutoPurge = Checkbutton(self.autoPurgeFrame,
                                        variable=self.chkVariable, 
                                        text="Auto Purge")
        self.rdoAutoPurge7 = Radiobutton(self.autoPurgeFrame, 
                                        text="Delete After 7 Days",
                                        variable=self.rdoVariable,
                                        value=2, state=DISABLED)
        self.rdoAutoPurge1 = Radiobutton(self.autoPurgeFrame, 
                                        text="Delete After 1 Day",
                                        variable=self.rdoVariable,
                                        value=1, state=DISABLED)
        self.rdoAutoPurge30 = Radiobutton(self.autoPurgeFrame, 
                                        text="Delete After 30 Days",
                                        variable=self.rdoVariable,
                                        value=4, state=DISABLED)
        self.rdoAutoPurgeCustom = Radiobutton(self.customPurgeFrame,
                                              text="Delete after X Days:",
                                              variable=self.rdoVariable,
                                              value=3, state=DISABLED)
        self.entVariable = StringVar()
        self.entAutoPurgeCustom = Entry(self.customPurgeFrame, width=3,
                                        state=DISABLED, 
                                        textvariable=self.entVariable)
        self.chkAutoPurge.bind('<Button-1>', self.toggleAutoPurgeEvent)
        self.autoPurgeFrame.bind('<Leave>', self.autoPurgeSetting)
        self.entAutoPurgeCustom.bind('<Button-1>', self.clickedCustom)
        self.autoPurgeState = (False, 0)
    
    def toggleAutoPurgeEvent(self,event,):
        self.toggleAutoPurge(False)  
        
    def toggleAutoPurge(self, checked):
        if self.chkVariable.get() == checked:
            self.rdoAutoPurge7.config(state=NORMAL)
            self.rdoAutoPurge1.config(state=NORMAL)
            self.rdoAutoPurgeCustom.config(state=NORMAL)
            self.entAutoPurgeCustom.config(state=NORMAL)
            self.rdoAutoPurge30.config(state=NORMAL)
            if not self.rdoVariable.get():
                self.rdoVariable.set(4)
        else:
            self.rdoAutoPurge1.config(state=DISABLED)
            self.rdoAutoPurge7.config(state=DISABLED)
            self.rdoAutoPurgeCustom.config(state=DISABLED)
            self.entAutoPurgeCustom.config(state=NORMAL)
            self.rdoAutoPurge30.config(state=DISABLED)
            
    def autoPurgeSetting(self, event):
        setting = self.rdoVariable.get()
        enabled = self.chkVariable.get()
        if setting == 1 and enabled:
            self.autoPurgeState = (True, 1)
        elif setting == 2 and enabled:
            self.autoPurgeState = (True, 7)
        elif setting == 3 and enabled:
            self.autoPurgeState = (True, int(self.entAutoPurgeCustom.get()))
        elif setting == 4 and enabled:
            self.autoPurgeState = (True, 30)
        else:
            self.autoPurgeState = (False, 0)
        self.saveOptions()

        
    def clickedCustom(self,event):
        if self.chkVariable.get() == 1:
            self.rdoVariable.set(3)
                           
    def saveOptions(self):
        self.settings['AutoPurge'] = self.autoPurgeState
        settingsJSON = json.dumps(self.settings)
        with open(self.filePath, "w") as output:
            output.write(settingsJSON)
        
    def loadOptions(self):
        if exists(self.filePath):
            with open(self.filePath) as input:
                settings = json.load(input)
                for item in settings:
                    self.settings[item] = settings[item]
        self.loadPurgeSettings()
        
    def loadPurgeSettings(self):
        purgeSettings = self.settings['AutoPurge']
        print(purgeSettings)
        if purgeSettings[0] == True:
            self.chkVariable.set(1)
            if purgeSettings[1] == 1:
                self.rdoVariable.set(1)
            elif purgeSettings[1] == 7:
                self.rdoVariable.set(2)
            elif purgeSettings[1] == 30:
                self.rdoVariable.set(4)
            else:
                self.rdoVariable.set(3)
                self.entVariable.set(int(purgeSettings[1]))
            self.toggleAutoPurge(True)
            
    def runPurge(self):
        if self.settings['AutoPurge'][0] == True:
            purgeDays = int(self.settings['AutoPurge'][1])
            endDate = date.today() + timedelta(days=-(purgeDays))
            foldersList = os.listdir(self.coverLetterDirectory)
            for i in foldersList:
                datedFolder = datetime.strptime(i, '%Y-%m-%d').date()
                if endDate > datedFolder:
                    print(f'{datedFolder} needs deleted')
                    deleteFolder = os.path.join(self.coverLetterDirectory + '\\' + i)
                    print(deleteFolder)
                    shutil.rmtree(deleteFolder)

    def packUI(self):
        self.pdfFrame.pack(side=TOP, pady=10, padx=2)
        self.saveFrame.pack(side=TOP, pady=10, padx=2)

        
        self.btnGeneratePDF.pack(pady=10)
        self.btnOpen.pack(pady=10)
        self.lblTemplate.pack(side=TOP, pady=5)
        self.btnSave.pack(padx=5,side=LEFT,pady=5)
        self.btnLoad.pack(padx=5,side=LEFT,pady=5)
        self.lblPurge.pack(side=TOP, pady=5, padx=2)
 
        self.chkAutoPurge.pack(side=TOP)
        self.rdoAutoPurge1.pack(side=TOP)
        self.rdoAutoPurge7.pack(side=TOP)
        self.rdoAutoPurge30.pack(side=TOP)
        self.customPurgeFrame.pack(side=TOP)
        self.rdoAutoPurgeCustom.pack(side=LEFT)
        self.entAutoPurgeCustom.pack(side=LEFT)
        self.btnPurgeOld.pack(side=TOP, pady=10)
        self.purgeFrame.pack(side=TOP, anchor=CENTER, padx=2)   
        self.autoPurgeFrame.pack(padx=2)
        
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
            