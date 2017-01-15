import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button

class storyWidget(Widget):
        def record(self):
                print ('Record button released. Implement backend here')

        def save(self):
                print ('Save button released. Implement backend here')

class storyApp(App):

        def build(self):
                #parent = Widget()
                #self.mainScreen = storyWidget()

                #rbtn = Button(text='Record')
                #sbtn = Button(text='Save')
                #rbtn.bind(on_release=self.record)
                #sbtn.bind(on_release=self.save)

                #parent.add_widget(self.mainScreen)
                #parent.add_widget(rbtn)
                #parent.add_widget(sbtn)
                
                return storyWidget()

if __name__ == '__main__':
        storyApp().run()
