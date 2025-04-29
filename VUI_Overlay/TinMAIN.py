import sys
import PyQt5.QtCore
import pyttsx3
import speech_recognition as sr
import datetime
import keyboard
import subprocess as sp
import os
import wikipedia
import pywhatkit
from googletrans import Translator,constants
import pyjokes
from pyautogui import moveTo,write,leftClick
from utils import send_email,search_on_google

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtGui
from PyQt5.QtCore import QThread
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow


from VUIoverlay import Ui_Overlay

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voices',voices[1].id)

state=None

def speak(audio):
    ui.updateGIF("speaking")
    engine.say(audio)
    engine.runAndWait()   


def wishings(self):
    ui.updateGIF("speaking")
    hour = int(datetime.datetime.now().hour)
    if hour >=0 and hour <12:
        ui.terminalprint("Good morning BOSS")
        speak("Good morning BOSS")
    elif hour >=12 and hour <17:
        ui.terminalprint("Good afternoon BOSS")
        speak("Good afternoon BOSS")
    elif hour >=17 and hour <21:
        ui.terminalprint("Good Evening BOSS")
        speak("Good Evening BOSS")
    else:
        ui.terminalprint("Good Night BOSS")
        speak("Good Night BOSS")

listening=True

def start_listening():
    global listening
    listening = True
    ui.terminalprint("started listening ")


def pause_listening():
    global listening
    listening = False
    ui.terminalprint("stopped listening")


keyboard.add_hotkey('ctrl+alt+k', start_listening)
keyboard.add_hotkey('ctrl+alt+p', pause_listening)




class TinMainClass(QThread):
    def __init__(self):
        super(TinMainClass, self).__init__()

    def run(self):
        self.runtintin()
        
       
    def commands(self):
        ui.updateGIF("listenting")
        r = sr.Recognizer()
        with sr.Microphone() as source:
            ui.terminalprint("Listening.......")
            r.pause_threshold = 1
            r.adjust_for_ambient_noise(source , duration=0)
            audio=r.listen(source)
        try:
            ui.updateGIF('loading')
            ui.terminalprint("Wait for few moments....") 
            self.query = r.recognize_google(audio, language='en-in')
            ui.terminalprint(f"You Just Said: {self.query}\n")
        except Exception as e:
            print(e)
            speak("Please tell me again")
            self.query="none"

        return self.query
    
    def Translation(self, tquery):
        tquery= tquery.replace('translate', '')
        translator = Translator()
        try:
            textTotranslate = translator.translate(tquery, src='en',dest = 'ta')
            text = textTotranslate.text
            pro = textTotranslate.pronunciation
            ui.terminalprint(pro + '=>' + text)
            speak(pro)
        except Exception as e:
            ui.terminalprint("Unable to Translate Sir")
            ui.terminalprint(e)
            speak("Unable to Translate Sir")


     
    def runtintin(self):
            wishings(self)
            while True:
                if listening:
                    self.query = self.commands().lower()
                    if 'time' in self.query:
                        strTime = datetime.datetime.now().strftime("%H:%M:%S")
                        str(strTime)
                        ui.terminalprint(strTime)
                        speak("Sir, The time is:" + strTime)
                    elif 'date' in self.query:
                        strdate = datetime.datetime.now().strftime("%d-%m-%Y")
                        speak("Sir, Today is :" + strdate)
                        ui.terminalprint(strdate)
                    elif 'open firefox' in self.query:
                        ui.terminalprint("Opening firefox sir")
                        speak("Opening firefox sir")
                        os.startfile("C:\\Program Files\\Mozilla Firefox\\firefox.exe")
                    elif 'translate' in self.query:
                        self.Translation(self.query)
                    elif 'open whatsapp' in self.query:
                        ui.terminalprint("Opening whatsapp")
                        speak("Opening whatsapp sir")
                        os.startfile("C:\\Program Files\\WindowsApps\\5319275A.WhatsAppDesktop_2.2450.6.0_x64__cv1g1gvanyjgm\\WhatsApp.exe")
                    elif 'open camera' in self.query:
                        ui.terminalprint("Opening camera sir")
                        speak("Opening camera sir")
                        sp.run('start microsoft.windows.camera:', shell=True)
                    elif 'wikipedia' in self.query or 'search' in self.query:
                        ui.terminalprint("Searching in wikipedia")
                        speak("Searching in wikipedia")
                        try:
                            self.query=self.query.replace("wikipedia",'')
                            self.query=self.query.replace("search",'')
                            results = wikipedia.summary(self.query, sentences=2)
                            speak("According to wikipedia....")
                            ui.terminalprint(results)
                            speak(results)
                        except:
                            ui.terminalprint("No results found.....")
                            speak("No results found")
                    elif "send an email" in self.query:
                        speak("On what email address do you want to send sir?. Please enter in the terminal")
                        receiver_add = input("Enter the Email ID")
                        speak("What should be the subject sir?")
                        subject = self.commands().capitalize()
                        speak("What is the message ?")
                        message = self.commands().capitalize()
                        if send_email(receiver_add, subject, message):
                            speak("I have sent the email sir")
                            ui.terminalprint("I have sent the email sir")
                        else:
                            speak("something went wrong Please check the error log")
                            ui.terminalprint("something went wrong Please check the error log")

                    elif 'play' in self.query:
                        self.query = self.query.replace("play", '')
                        speak("Playing "+ self.query)
                        pywhatkit.playonyt(self.query)

                    elif 'type' in self.query or 'notepad' in self.query:
                        speak("Please tell me what should I write")
                        while True:
                            writeinnotepad = self.commands()
                            if writeinnotepad == "exit typing":
                                speak("Done sir")
                            else:
                                write(writeinnotepad)
                    elif 'minimize' in self.query or 'minimise' in self.query:
                        moveTo(1800,15)
                        leftClick()

                    elif 'close window' in self.query :
                        moveTo(1900,15)
                        leftClick()


                    elif 'joke' in self.query:
                        tintinjoke = pyjokes.get_joke()
                        ui.terminalprint(tintinjoke)
                        speak(tintinjoke)

                    elif 'exit program' in self.query or 'exit the program' in self.query or 'bye tintin' in self.query:
                        ui.terminalprint("I'm Leaving Sir, Byeee.....")
                        speak("I'm Leaving Sir, Bye")
                        quit()


startExecution= TinMainClass()


class Ui_jarvis(QMainWindow):
    def __init__(self):
        super(Ui_jarvis, self).__init__()
        self.oldPosition= PyQt5.QtCore.QPoint
        self.JarvisUI = Ui_Overlay()
        self.JarvisUI.setupUi(self)
        self.showstatusicons = False

        self.JarvisUI.showstatusicons.stateChanged.connect(self.showicontoggle)
        self.JarvisUI.showterminal.stateChanged.connect(self.showterminaltoggle)
        self.JarvisUI.mutejarvis.stateChanged.connect(self.mutejarvisCB)
        self.JarvisUI.customsearch.stateChanged.connect(self.customsearchframe)

        self.JarvisUI.VUIlogoButton.clicked.connect(lambda: self.changeminsize('full'))
        self.JarvisUI.exitbutton.clicked.connect(self.close)
        self.JarvisUI.minimize.clicked.connect(lambda: self.changeminsize('min'))
        self.JarvisUI.sendbutton.clicked.connect(self.manualcodefromterminal)
        self.runallgif()

        startExecution.start()

    def customsearchframe(self, checked):
        if checked:
            self.showsearch = True
            self.JarvisUI.frame_2.show()
        else:
            self.showsearch = False
            self.JarvisUI.frame_2.hide()


    def mutejarvisCB(self, checked):
        if checked:
            pause_listening()
        else:
            start_listening()

    def showterminaltoggle(self, checked):
        if checked:
            self.showTerminal=True
            self.changeminsize('full')
        else:
            self.showTerminal = True
            self.resize(398,180)

    def showicontoggle(self, checked):
        if checked:
            self.showstatusicons = True
        else:
            self.showstatusicons = False

    def changeminsize(self,type):
        if type== 'full':
            self.resize(541,437)
        elif type== 'min':
            if not self.showstatusicons:
                self.resize(151,60)
        else:
            self.resize(141,211)

    def mousePressEvent(self, event):
        self.oldPosition = event.globalPos()

    def mouseMoveEvent(self, event):
        d = PyQt5.QtCore.QPoint(event.globalPos() - self.oldPosition)
        self.move(self.x() + d.x(), self.y() + d.y())
        self.oldPosition = event.globalPos()

    def runallgif(self):
        self.JarvisUI.listentingmovie=QtGui.QMovie("D:/Ai Generator/RESOURCES/listen.gif")
        self.JarvisUI.listenting.setMovie(self.JarvisUI.listentingmovie)
        self.JarvisUI.listentingmovie.start()

        self.JarvisUI.loadingmovie=QtGui.QMovie("D:/Ai Generator/RESOURCES/loading.gif")
        self.JarvisUI.loading.setMovie(self.JarvisUI.loadingmovie)
        self.JarvisUI.loadingmovie.start()

        self.JarvisUI.speakingmovie=QtGui.QMovie("D:/Ai Generator/RESOURCES/speaking.gif")
        self.JarvisUI.speaking.setMovie(self.JarvisUI.speakingmovie)
        self.JarvisUI.speakingmovie.start()

    def updateGIF(self, state):
        if state=='speaking':
            self.JarvisUI.speaking.raise_()
            self.JarvisUI.speaking.show()
            self.JarvisUI.listenting.hide()
            self.JarvisUI.loading.hide()

        elif state=='listenting':
            self.JarvisUI.listenting.raise_()
            self.JarvisUI.listenting.show()
            self.JarvisUI.speaking.hide()
            self.JarvisUI.loading.hide()

        elif state=='loading':
            self.JarvisUI.loading.raise_()
            self.JarvisUI.loading.show()
            self.JarvisUI.listenting.hide()
            self.JarvisUI.speaking.hide()

    def terminalprint(self, text):
        self.JarvisUI.terminal.appendPlainText(text)

    def manualcodefromterminal(self):
        if self.JarvisUI.lineEdit.text():
            cmd= self.JarvisUI.lineEdit.text()
            self.JarvisUI.lineEdit.clear()
            self.JarvisUI.terminal.appendPlainText(f"You typed->> {cmd}")

    




        

        





if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = Ui_jarvis()
    ui.show()
    sys.exit(app.exec_())
