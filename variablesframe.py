from tkinter.constants import BOTH, CENTER, DISABLED, LEFT, YES
from tkinter.font import NORMAL
from tkinter import Label, Entry, Button, Frame, StringVar
from datetime import date
import os
from os.path import exists
import json

from window import MainWindow


class VariablesFrame(MainWindow):

    def __init__(self, change=False):
        MainWindow.__init__(self)
        self.changeName = change
        self.createFrame()
        self.assignUI()
        self.personalInfo = {
            "Name": '',
            "Address": '',
            "Phone": '',
            "Email": '',
            "Website": ''
        }
        self.loadInfo()
        
    def createFrame(self):
        self.frame = Frame(self.mainFrame, 
                           height = 100)    
           
    def assignUI(self):
        todaysDate = date.today().strftime("%m-%d-%Y")
        self.lblKeyWords = Label(self.frame,
                                 text = "Keywords to be Replaced",
                                 font = ('Helvetica 15 underline')) 
        self.companyFrame = Frame(self.frame, 
                                  height=100, 
                                  highlightbackground='black', 
                                  highlightthickness=1)
        self.companyName = StringVar(self.frame)
        self.companyNameLbl = Label(self.companyFrame, 
                                    text = "Company Name / COMPANY")
        self.companyNameEnt = Entry(self.companyFrame, 
                                    textvariable = self.companyName, 
                                    justify = CENTER, 
                                    highlightbackground='red', 
                                    highlightthickness=1)
        self.positionName = StringVar(self.frame)
        self.positionLbl = Label(self.companyFrame, 
                                 text = "Position / POSITION")
        self.positionEnt = Entry(self.companyFrame, 
                                 textvariable = self.positionName, 
                                 justify = CENTER, 
                                 highlightbackground='red', 
                                 highlightthickness=1)
        
        self.nameFrame = Frame(self.frame, 
                               height=100, 
                               highlightbackground='black', 
                               highlightthickness=1)
        self.date = StringVar(self.frame, 
                              todaysDate)
        self.dateLbl = Label(self.nameFrame, 
                             text = "Date / DATE ")
        self.dateEntry = Entry(self.nameFrame, 
                               textvariable = self.date, 
                               state = DISABLED, 
                               justify = CENTER)
        self.yourName = StringVar(self.frame)
        self.nameLbl = Label(self.nameFrame, 
                             text = "Your Name / YOURNAME ")
        self.nameEntry = Entry(self.nameFrame, 
                               textvariable = self.yourName, 
                               justify = CENTER)
        self.btnUpdateName = Button(self.nameFrame, 
                                    text = "Edit Name", 
                                    command = self.enableName)
        self.btnSaveName = Button(self.nameFrame, 
                                  text = "Save Name", 
                                  command = self.disableName)

        self.headerFrame = Frame(self.frame, 
                                 height=100, 
                                 highlightbackground='black', 
                                 highlightthickness=1)
        self.lblHeader = Label(self.headerFrame, 
                               text = "Optional Header Information", 
                               font = ('Helvetica 12 underline'))
        self.city = StringVar(self.frame)
        self.lblCityState = Label(self.headerFrame, 
                                  text = "City")
        self.entCityState = Entry(self.headerFrame, 
                                  textvariable = self.city)
        self.phone = StringVar(self.frame)
        self.lblPhone = Label(self.headerFrame, 
                              text = "Phone Number")
        self.entPhone = Entry(self.headerFrame, 
                              textvariable = self.phone)
        self.email = StringVar(self.frame)
        self.lblEmail = Label(self.headerFrame, 
                              text = "Email Address")
        self.entEmail = Entry(self.headerFrame, 
                              textvariable = self.email)
        self.website = StringVar(self.frame)
        self.lblWebsite = Label(self.headerFrame, 
                                text = "Website")
        self.entWebsite = Entry(self.headerFrame, 
                                textvariable = self.website)
        self.optionalButtonFrame = Frame(self.headerFrame)
        self.btnOptionalEdit = Button(self.optionalButtonFrame, 
                                      text="Edit", 
                                      command=self.enablePersonal)
        self.btnOptionalSave = Button(self.optionalButtonFrame, 
                                      text="Save", 
                                      command=self.disablePersonal)

    def packUI(self):
        self.lblKeyWords.pack()
        self.nameFrame.pack(pady=10)
        self.companyFrame.pack(pady=10)
        self.dateLbl.pack()
        self.dateEntry.pack()
        self.companyNameLbl.pack(padx=10)
        self.companyNameEnt.pack(padx=10, 
                                 pady=10)
        self.positionLbl.pack(padx=10)
        self.positionEnt.pack(padx=10, 
                              pady=10)
        self.nameLbl.pack()
        self.nameEntry.pack()
        self.btnUpdateName.pack(side = LEFT, 
                                padx=10, 
                                pady=10)
        self.btnSaveName.pack(side = LEFT, 
                              padx=10, 
                              pady=10)
        self.headerFrame.pack(pady=50)
        self.lblHeader.pack(pady=10)
        self.lblCityState.pack()
        self.entCityState.pack(pady=10)
        self.lblPhone.pack()
        self.entPhone.pack(pady=10)
        self.lblEmail.pack()
        self.entEmail.pack(pady=10)
        self.lblWebsite.pack()
        self.entWebsite.pack(pady=10)
        self.btnOptionalEdit.pack(side=LEFT, padx=5)
        self.btnOptionalSave.pack(side=LEFT, padx=5)
        self.optionalButtonFrame.pack(pady=10)
        self.frame.pack(side = LEFT, expand = YES, 
                        fill = BOTH, pady=10)
        
    def enableName(self):
        self.nameEntry.configure(state=NORMAL)

    def disableName(self):
        self.nameEntry.configure(state=DISABLED)
        self.saveInfo()

    def enablePersonal(self):
        self.entCityState.configure(state=NORMAL)
        self.entEmail.configure(state=NORMAL)
        self.entPhone.configure(state=NORMAL)
        self.entWebsite.configure(state=NORMAL)
        self.nameLbl.configure(state=NORMAL)
        
    def disablePersonal(self):
        self.entCityState.configure(state=DISABLED)
        self.entEmail.configure(state=DISABLED)
        self.entPhone.configure(state=DISABLED)
        self.entWebsite.configure(state=DISABLED)
        self.nameLbl.configure(state=DISABLED)
        self.saveInfo()
        
    def getDate(self):
        return self.date.get()
    
    def getName(self):
        return self.yourName.get()
    
    def getPosition(self):
        return self.positionName.get()
    
    def getCompany(self):
        return self.companyName.get()
    
    def verifyDirectory(self):
        self.directory = os.getcwd()
        dataDirectory = os.path.join(self.directory, "Data")
        if exists(dataDirectory):
            pass
        else:
            os.mkdir(dataDirectory)
        self.filePath = os.path.join(self.directory, 
                                     "Data/personalinfo.json")
        
    def saveInfo(self):
        self.personalInfo['Name'] = self.yourName.get()
        self.personalInfo['Address'] = self.city.get()
        self.personalInfo['Phone'] = self.phone.get()
        self.personalInfo['Email'] = self.email.get()
        self.personalInfo['Website'] = self.website.get()

        self.verifyDirectory()
        infoJSON = json.dumps(self.personalInfo)
        with open(self.filePath, "w") as output:
            output.write(infoJSON)
    
    def getHeaderText(self):
        headerText = ''
        if self.city.get() != "":
            headerText += self.city.get() + ' | '
        if self.phone.get() != "":
            headerText += self.phone.get() + ' | '
        if self.email.get() != "":
            headerText += self.email.get() + ' | '
        if self.website.get() != "":
            headerText += self.website.get() + ' | '
        return headerText[0:-3]
    
    def loadInfo(self):
        self.verifyDirectory()
        if exists(self.filePath):
            with open(self.filePath) as input:
                info = json.load(input)
                for item in info:
                    self.personalInfo[item] = info[item]
        self.yourName.set(self.personalInfo['Name'])
        self.city.set(self.personalInfo['Address'])
        self.phone.set(self.personalInfo['Phone'])
        self.email.set(self.personalInfo['Email'])
        self.website.set(self.personalInfo['Website'])
        if self.yourName.get() != "":
            self.disableName()
        self.disablePersonal()
                    

if __name__ == "__main__":
    VariablesFrame()