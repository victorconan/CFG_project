import pyttsx
import os
import string
import speech
import speech_recognition as sr

# copied from GitHub
def record():
        # the record button is pressed
        # obtain audio from the microphone
        r = sr.Recognizer()
        with sr.Microphone() as source:
                print("Recording...:")
                audio = r.listen(source)

        # recognize speech using Google Speech Recognition
        try:
                rcdng = r.recognize_google(audio)
        except sr.UnknownValueError:
                print("We're sorry, but we couldn't recognize what you said")
        except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition$

        return audio, rcdng

def initEng():
        eng = pyttsx.init()
        eng.setProperty('rate', 70)
        return eng

def playback(eng, rcdng):
        # must print to GUI
        eng.say(rcdng)
        eng.runAndWait()

# How does this connect? Applies to all methods but main below this line
def pause(eng, rcdng):
        # eng is an engine object
        # is it possible to stop in the middle of a say command?
        if eng.isBusy() == True:
                eng.stop()
        modRcdng(rcdng)

def modRcdng(rcdng):
        # modify rcdng so we start talking in the right place
        
def gotoStart(eng):
        if eng.isBusy() == True:
                eng.stop()

# copied from GitHub
def save(audio):
        # again everything needs to connect to the GUI
        fname = input("What is your file name? ")

        # write audio to WAV file
        with open(fname, "wb") as f:
                f.write(audio.get_wav_data())

def changeVoice(eng):
        voices = eng.getProperty('voices')
        # print voices to GUI - for now, just plain print
        print ("Voices: ")
        print (voices)
        # User selects one via mouse click

def main():

        dir_path = os.path.dirname(os.path.realpath(__file__))
        print (dir_path)

        # test for different button presses
        # if statements
