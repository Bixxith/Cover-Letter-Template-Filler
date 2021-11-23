from coverletterwindow import CoverLetterWindow
from namewindow import NameWindow
import os
from os.path import exists

def namePathExists():
    path = os.path.join(os.getcwd(), "name.txt")
    return exists(path)

def main():
    if namePathExists():
        CoverLetterWindow()
    else:
        NameWindow()
        

if __name__ == '__main__':
    main()        


