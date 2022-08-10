import os.path

import requests
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.picker import MDDatePicker
from kivymd.uix.picker import MDThemePicker
from hashlib import sha256, md5
from kivy.animation import Animation


class Dez(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = Builder.load_file('dez.kv')
        menu_items = self.read_files_type('manufacturers.txt')
        menu_items_dez = self.read_files_type('typedez.txt', 1)
        self.menu = MDDropdownMenu(
            caller=self.screen.ids.proizv,
            items=menu_items,
            position="bottom",
            width_mult=4,
        )
        self.typedez = MDDropdownMenu(
            caller=self.screen.ids.type,
            items=menu_items_dez,
            position="bottom",
            width_mult=4,
        )
        self.date_dialog = MDDatePicker(background_color=(0.1, 0.1, 0.1, 1.0))
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
        self.icon = 'mascot.png'
        self.theme_cls.primary_palette = "BlueGray"
        self.theme_cls.primary_hue = "300"
        self.theme_cls.theme_style = "Light"
        return self.screen

    def rec_to_base(self):
        p_json = self.accum_fields()
        p_json['token_flask'] = "0516e4d8c9c108df2695a18c084185dc7acca45ef4e643b39c9bdc296b6848ee"
        json_param = p_json
        check = requests.post('http://37.77.105.58:5000/checkcode', json=json_param)
        if check.status_code == 200:
            self.show_information_dialog("Запись уже существует!")
            return False
        resp = requests.post('http://37.77.105.58:5000/create', json=json_param)
        print(resp)
        if resp.status_code == 200:
            self.show_information_dialog("Запись прошла успешно!")
            self.clear_fileds()
            if len(p_json['manufacturer']) > 0:
                self.write_files_type('manufacturers.txt', p_json['manufacturer'].strip())
                menu_items = self.read_files_type('manufacturers.txt')
                self.menu.items = menu_items
            if len(p_json['type']) > 0:
                self.write_files_type('typedez.txt', p_json['type'].strip())
                menu_items_dez = self.read_files_type('typedez.txt')
                self.typedez.items = menu_items_dez
        else:
            self.show_information_dialog("Ошибка записи!" + " " + str(resp.status_code))
            # self.clear_fileds()
            return False
        return True

    def accum_fields(self, status=0):
        list_f = []
        hash_str = ''
        for i in self.screen.ids:
            try:
                str_v = self.screen.ids[i].text.strip()
                if len(str_v) > 0:
                    hash_str = hash_str + str_v[0:35]
                    list_f.append(str_v)
                else:
                    list_f.append("")
            except:
                pass
        hash_object = md5(hash_str.encode())
        p_dict = {'code': hash_object.hexdigest()}
        pp_list = ['type', 'manufacturer', 'name', 'structure', 'used', 'expiration_date', 'packing', 'comment']

        for i, y in enumerate(pp_list):
            p_dict[y] = list_f[i]

        if status > 0:
            return hash_object.hexdigest()
        # l = list_f.insert(0,hash_object.hexdigest())
        return p_dict

    def show_information_dialog(self, text):
        OKButton = MDFlatButton(text="ОК", text_color=self.theme_cls.primary_color, on_release=self.close_dialog)
        self.dialog = MDDialog(
            text=text,
            buttons=[
                OKButton
            ],
        )
        self.dialog.open()

    def close_dialog(self, obj):
        self.dialog.dismiss()

    def clear_fileds(self):
        for i in self.screen.ids:
            try:
                str_v = self.screen.ids[i].text.strip()
                if len(str_v) > 0:
                    self.screen.ids[i].text = ""
            except:
                pass

    def show_theme_picker(self):
        theme_dialog = MDThemePicker()
        theme_dialog.open()

    def read_files_type(self, p_file, status=0):
        if not os.path.exists(p_file):
            return []
        with open(p_file, "r", encoding="utf-8") as file:
            contents = file.readlines()
            if status == 0:
                ret = [{"icon": "git", "text": f"{y}", "viewclass": "OneLineListItem",
                        "on_release": lambda x=y: self.set_item(x)} for i, y in enumerate(contents)]
            else:
                ret = [{"icon": "git", "text": f"{y}", "viewclass": "OneLineListItem",
                        "on_release": lambda x=y: self.set_item_dez(x)} for i, y in enumerate(contents)]
        return ret

    def write_files_type(self, p_file, text):
        if not os.path.exists(p_file):
            return False
        with open(p_file, "a", encoding="utf-8") as file:
            contents = file.write(text + "\n")
        return True

    def set_token(self, p_text):
        if not os.path.exists('token.txt'):
            f = open('token.txt', "x", encoding="utf-8")
            f.close()

        with open('token.txt', "w+", encoding="utf-8") as file:
            file.write('')
            file.seek(0)
            file.write(sha256(p_text.encode('utf-8')).hexdigest())
            file.close()
        self.screen.ids['token'].text = ""
        return True

    def start_animation(self):
        lbl_1 = self.root.ids.lbl_1

        Animation(
            opacity=1, y=lbl_1.height * 2, d=0.9, t="out_elastic"
        ).start(lbl_1)



Dez().run()
