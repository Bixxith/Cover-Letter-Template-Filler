from coverletterwindow import CoverLetterWindow

import os
from os.path import exists

def namePathExists():
    path = os.path.join(os.getcwd(), "name.txt")
    return exists(path)

def main():
    mainWin = CoverLetterWindow()

        

if __name__ == '__main__':
    main()        


