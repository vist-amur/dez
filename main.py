from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.core.window import Window
#from tkinter import *

# root = Tk()
# monitor_height = root.winfo_screenheight()
# monitor_width = root.winfo_screenwidth()


Window.maximize()
#Window.size = (monitor_width , monitor_height)

class Container(MDBoxLayout):
    def func(self):
            print('ssss')

class Dez(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Indigo"
        return Container()

Dez().run()