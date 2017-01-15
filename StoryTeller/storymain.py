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
class Root(BoxLayout):
    pass


class RecordButton(Button):
    #hold output for displaying by Textinput
    output = StringProperty('')
    
    def record(self):
        #audio capture
        with m as source:
            audio = r.listen(source)
        
        try:
            #recognize speech using Google Speech Recognition
            value = r.recognize_google(audio)
            self.output = "Your story:\n{}".format(value)
        
        except sr.UnknownValueError:
            self.output = ("Oops! Didn't catch that")
        
        except sr.RequestError as e:
            self.output = ("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))

class PlayButton(Button):
    #take the value from the text input and play it as audio
    def play(self,text):
        engine = px.init()
        engine.say(text)
        engine.runAndWait()
        

class StoryApp(App):
    def build(self):
        #Calibrate the Microphone to Silent Levels
        print("A moment of silence, please...")
        with m as source:
            r.adjust_for_ambient_noise(source)
            print("Set minimum energy threshold to {}".format(r.energy_threshold))
        
        return Root()


#Execute from the command line
if __name__ == '__main__':
    StoryApp().run()
