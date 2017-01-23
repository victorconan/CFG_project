from kivy.config import Config
Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '400')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.properties import StringProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.properties import ListProperty
from kivy.uix.popup import Popup

import os
import random

import speech_recognition as sr
import pyttsx as px

r = sr.Recognizer()
m = sr.Microphone()

# Root Widget
class Root(FloatLayout):
    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()
        
    def show_save(self):
        content = SaveDialog(save=self.save, cancel=self.dismiss_popup)
        self._popup = Popup(title="Save file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename):
        with open(os.path.join(path, filename[0])) as stream:
            self.text_input.text = stream.read()

        self.dismiss_popup()
        
    def save(self, path, filename):
        with open(os.path.join(path, filename), 'w') as stream:
            stream.write(self.output)

        self.dismiss_popup()

    #hold output for displaying by Textinput
    output = StringProperty('Your story:\n')
    record_buttion_disabled = False
    def record(self):
        global stop_listening
        #audio capture
        #with m as source:
        #    audio = r.listen_in_background(source, callback)
        record_button_disabled = True
        self.ids['record_button'].disabled=record_button_disabled
        def callback(r, audio):
            try:
                #recognize speech using Google Speech Recognition
                value = r.recognize_google(audio)
                self.output += "{}\n".format(value)
            
            except sr.UnknownValueError:
                self.output = ("Oops! Didn't catch that")
            
            except sr.RequestError as e:
                self.output = ("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
        stop_listening = r.listen_in_background(m, callback, phrase_time_limit=20)
        
    #take the value from the text input and play it as audio
    def play(self,text):
        engine = px.init()
        engine.say(text)
        engine.runAndWait()

    def pause(self):
        #stop_listening = r.listen_in_background(m, callback)
        stop_listening()
        record_button_disabled = False
        self.ids['record_button'].disabled=record_button_disabled

    text_size = ObjectProperty('18pt')
    def text_large(self):
        increment = 5
        self.text_size = str(int(self.text_size[:-2])+increment)+'pt'

    def text_small(self):
        increment = 5
        self.text_size = str(int(self.text_size[:-2])-increment)+'pt'

    text_color = ListProperty([0,0,0,1])
    def text_change_color(self):
        r = random.random()
        g = random.random()
        b = random.random()
        self.text_color = [r,g,b,1]


class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)

class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)
    

class Story2App(App):
    def build(self):
        #Calibrate the Microphone to Silent Levels
        print("A moment of silence, please...")
        with m as source:
            r.adjust_for_ambient_noise(source)
            print("Set minimum energy threshold to {}".format(r.energy_threshold))
        
        pass

Factory.register('Root', cls=Root)
Factory.register('LoadDialog', cls=LoadDialog)
Factory.register('SaveDialog', cls=SaveDialog)

#Execute from the command line
if __name__ == '__main__':
    Story2App().run()
