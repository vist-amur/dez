from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.core.window import Window
from kivymd.uix.menu import MDDropdownMenu
from kivy.lang import Builder
from kivymd.uix.pickers import MDDatePicker
import datetime
#from tkinter import *

# root = Tk()
# monitor_height = root.winfo_screenheight()
# monitor_width = root.winfo_screenwidth()

#Window.maximize()
#Window.size = (monitor_width , monitor_height)

# class Container(MDBoxLayout):
#     def func(self):
#             print('ssss')

class Dez(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = Builder.load_file('dez.kv')
        menu_items = [{"icon": "git", "text": f"Item {i}","viewclass": "OneLineListItem", "on_release": lambda x=f"Item {i}": self.set_item(x)} for i in range(5)]
        self.menu = MDDropdownMenu(
            caller=self.screen.ids.proizv,
            items=menu_items,
            position="bottom",
            width_mult=4,
        )
        self.date_dialog = MDDatePicker(background_color=(0.1,0.1,0.1,1.0))
        self.menu.bind()
        self.date_dialog.bind(on_save=self.on_save_date, on_cancel=self.on_cancel_date)



    def on_save_date(self, instance, value, date_range):
        self.screen.ids.expiration.text = str(value)

    def on_cancel_date(self, instance, value):
        pass

    def set_item(self, instance):
        self.screen.ids.proizv.text = instance
        self.menu.dismiss()

    def build(self):
        self.theme_cls.primary_palette = "Indigo"
        return self.screen

Dez().run()