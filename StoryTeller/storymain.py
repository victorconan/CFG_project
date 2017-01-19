from kivy.config import Config
Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '400')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.properties import StringProperty

import speech_recognition as sr
import pyttsx as px

r = sr.Recognizer()
m = sr.Microphone()


# Root Widget
output = None
outputsize = None
savenum = 1
class Root(BoxLayout):
    pass

class RecordButton(Button):
    #hold output for displaying by Textinput
    output = StringProperty('')

    #other variables
    if outputsize == None:
        outputsize = '16dp'

    def record(self):
        self.outputsize = outputsize
        self.savenum = int(savenum)
        
        #audio capture
        with m as source:
            audio = r.listen(source)

        try:
            #recognize speech using Google Speech Recognition
            value = r.recognize_google(audio)
            self.output = "Your story:\n{}".format(value)

        except sr.UnknownValueError:
            self.output = ("Story Teller didn't catch that")
            #value = Label(text='Story Teller didn\'t catch that')

        except sr.RequestError as e:
            self.output = ("Story Teller couldn't request results from Google Speech Recognition service; {0}".format(e))
            #preval = 'Story Teller couldn\'t request results from Google Speech Recognition service; {0}'.format(e)
            #value = Label(text=preval)

        output = self.output
        self.saveAud(audio)

    def saveAud(self, audio):
        s = int((self.savenum+1)/2)
        fname = "audio" + str(s) + ".wav"
        with open(fname, "wb") as f:
                f.write(audio.get_wav_data())

        self.savenum += 1
        self.saveTxt()

    def saveTxt(self):
        s = int(self.savenum/2)
        fname = "text" + str(s) + ".txt"
        with open(fname, 'w') as f:
            f.write(self.output)

        self.savenum += 1
        global savenum
        savenum = self.savenum #updates global variable


class PlayButton(Button):
    #take the value from the text input and play it as audio
    def play(self,text):
        engine = px.init()
        engine.say(text)
        engine.runAndWait()

class SmallButton(Button):
    #make text small
    def small(self,text):
        outputsize = '12dp'
        #do we need to refresh?

class StoryApp(App):
    def build(self):
        #Calibrate the Microphone to Silent Levels
        print("A moment of silence, please...")
        with m as source:
            print("Set minimum energy threshold to {}".format(r.energy_threshold))

        return Root()


#Execute from the command line
if __name__ == '__main__':
    StoryApp().run()