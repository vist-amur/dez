from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.core.window import Window
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.dialog import MDDialog
from kivy.lang import Builder
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.button import MDFlatButton
import datetime
import pymysql
import hashlib
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
        menu_items_dez = [{"icon": "git", "text": f"Item {i}", "viewclass": "OneLineListItem",
                       "on_release": lambda x=f"Item {i}": self.set_item_dez(x)} for i in range(9)]
        self.menu = MDDropdownMenu(
            caller=self.screen.ids.proizv,
            items=menu_items,
            position="bottom",
            width_mult=4,
        )
        self.typedez = MDDropdownMenu(
            caller=self.screen.ids.proizv,
            items=menu_items_dez,
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

    def set_item_dez(self, instance):
        self.screen.ids.type.text = instance
        self.typedez.dismiss()

    def build(self):
        self.theme_cls.primary_palette = "Indigo"
        return self.screen

    def rec_to_base(self):
        p_addressDB = '37.77.105.58'
        p_loginDB = 'phpmyadmin'
        p_passDB = 'g7A1PuDN'
        p_nameDB = 'dezreestr'
        p_nametable = 'dez'

        connection = pymysql.connect(host=p_addressDB, user=p_loginDB, passwd=p_passDB, database=p_nameDB)

        try:
            cursor = connection.cursor()
            hash_field = self.accum_fields(1)
            p_list = self.accum_fields()
            sql = f"Select * from {p_nametable} where code LIKE '{hash_field}'"
            cursor.execute(sql)

            oneRow = cursor.fetchone()

            if oneRow == None:
                cursor = connection.cursor()
                sql = f'INSERT INTO {p_nametable} (code, type, manufacturer, name, ' \
                      'structure, used, expiration_date, packing, ' \
                      'comment) ' \
                      'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                cursor.execute(sql, (hash_field, p_list[0], p_list[1], p_list[2], p_list[3],p_list[4],p_list[5],p_list[6],p_list[7]))
                connection.commit()
                self.show_information_dialog("Запись прошла успешно!")
            else:
                self.show_information_dialog("Такая запись уже существует!")
        except:
            connection.close()
            # with open(r'D:\trace.txt', 'a') as fp:
            #    traceback.print_exc(file=fp)
            # повторный вызов исключения, если это необходимо.
            raise


        try:
            connection.close()
        except:
            # print('Connected was closed!')
            pass

    def accum_fields(self, status=0):
        list_f = []
        hash_str = ''
        for i in self.screen.ids:
            try:
                str_v = self.screen.ids[i].text.strip()
                if len(str_v) > 0:
                    hash_str = hash_str + str_v[0:3]
                    list_f.append(str_v)
            except:
                pass
        #print(list_f)

        hash_object = hashlib.md5(hash_str.encode())
        if status > 0:
            return hash_object.hexdigest()
        #l = list_f.insert(0,hash_object.hexdigest())
        return list_f

    def show_information_dialog(self, text):
        OKButton  = MDFlatButton(text="ОК", text_color=self.theme_cls.primary_color, on_release=self.close_dialog)
        self.dialog = MDDialog(
            text=text,
            buttons=[
                OKButton
            ],
        )
        self.dialog.open()

    def close_dialog(self, obj):
        self.dialog.dismiss()

Dez().run()