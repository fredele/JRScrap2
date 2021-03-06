
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals

import os

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager
from kivy.config import Config
from kivy.uix.dropdown import DropDown
from restapi.mcws import MCWS
from screens.player import PlayerScreen
from screens.filesstack import FilesStackScreen
from screens.fieldsstack import FieldsStackScreen
from widgets.filesstack import FilesStackWidget
from widgets.fieldsstack import FieldsStackWidget
from settings.password import SettingPassword
from kivy.storage.jsonstore import JsonStore
from kivy.logger import Logger
from kivy import utils
from kivy.core.window import Window
from os.path import join
import json


class ScreenManager(ScreenManager):
    def __init__(self):
        super(ScreenManager, self).__init__()
        self.app = App.get_running_app()

    def GotoPlayerScreen(self):
        self.current = 'PlayerScreen'

    def GotoFilesStackScreen(self):
        self.current = 'FilesStackScreen'
        print(self.app.search)
        if self.app.search == "Current selection":
            self.app.FilesStackWidget.GetCurrentSelectedFiles()
        else:
            self.app.FilesStackWidget.SearchFiles(self.app.search)
            for index in self.app.searches:
                if index["search"] == self.app.search:
                    self.app.FilesStackScreen.ids.selectsearch.text = index["name"]

    def GotoFieldsStackScreen(self):
        self.current = 'FieldsStackScreen'


class JRScrap2App(App):
    Schedule_time = 1

    def on_stop(self):
        Window.close()
        return True

    def __init__(self):
        super(JRScrap2App, self).__init__()
        self.platform = utils.platform
        Logger.debug('PLATEFORM : ' + self.platform)

        self.app = App.get_running_app()
        self.root_dir = os.path.dirname(os.path.realpath(__file__))
        Config.read(os.path.join(self.root_dir, 'debug.ini'))
        self.jsondata = """
[
        {
        "type": "string",
        "title": "Host",
        "section": "MCWS",
        "key": "host"
        },
        {
        "type": "string",
        "title": "Port",
        "section": "MCWS",
        "key": "port"
        },
        {
        "type": "title",
        "title": "Authentication"
        },
        {
        "type": "string",
        "title": "Username",
        "section": "MCWS",
        "key": "admin"
        },
        {
        "type": "password",
        "title": "Password",
        "section": "MCWS",
        "key": "password"
        },
        {
        "type": "title",
        "title": "Settings"
        },
         {
        "type": "options",
        "title": "Language",
        "desc": "Set the language for the APIs",
        "section": "MCWS",
        "key": "language"
        },
        {
        "title": "Date",
        "section": "MCWS",
        "key": "date",
        "type": "options",
        "options": ["%d/%m/%Y", "%Y-%m-%d","%m-%d-%Y"],
        "desc": "Set the date display format"},

        {
        "type": "options",
        "title": "Thumbnail Size",
        "desc": "Set the JRMC Thumbnail Size to display",
        "section": "MCWS",
        "key": "thumbnail_size",
        "options":["Small","Medium","Large"]
       },
       {
        "type": "string",
        "title": "Files per page",
        "desc": "Set the Nbrs. of files per page to display",
        "section": "MCWS",
        "key": "filesperpage"
        },
        {
        "type": "title",
        "title": "Multi Scrap"
        },
        {
        "type": "bool",
        "title": "Cover Art",
        "desc": "Save Cover Art on Mass Scrap",
        "section": "MCWS",
        "key": "cover_art",
        "true": "auto"
        }

]
"""

        # Add the different languages to the settings

        optlang = []

        self.StoreLanguages = JsonStore(join(self.root_dir + "/json/", "languages.json"))
        if self.StoreLanguages.exists('languages'):
            self.Languages = self.StoreLanguages.get('languages')
        for language in self.Languages:
            optlang.append(language)

        jsondata_py = json.loads(self.jsondata)
        for item in jsondata_py:
            if "key" in item:
                if item["key"] == "language":
                    item["options"] = optlang
        self.jsondata = json.dumps(jsondata_py)

        # Set the Searches for the FilesWidget
        self.StoreSearches = JsonStore(join(self.root_dir + "/json/", "searches.json"))
        if self.StoreSearches.exists('searches'):
            self.searches = self.StoreSearches.get('searches')

        # Set the App. params.
        self.store = JsonStore(join(self.root_dir + "/json/", "params.json"))

    def build(self):

        self.lang = self.app.config.getdefault("MCWS", "language", "EN")
        self.DateFormat = self.app.config.getdefault("MCWS", "date", "%d/%m/%Y")
        self.CoverArtMassScrap = self.app.config.getdefault("MCWS", "cover_art", "0")
        self.thumbnail_size = self.app.config.getdefault("MCWS", "thumbnail_size", "Medium")
        MCWS_port = self.config.getdefault("MCWS", "port", "52199")
        MCWS_host = self.config.getdefault("MCWS", "host", "localhost")
        self.filesperpage = self.config.getdefault("MCWS", "filesperpage", "50")


        # Add widgets to ScreenManager
        self.ScreenManager = ScreenManager()

        self.FilesStackScreenControlWidget = FilesStackScreen(name='FilesStackScreen')
        self.ScreenManager.add_widget(self.FilesStackScreenControlWidget)
        self.FieldsStackScreenControlWidget = FieldsStackScreen(name='FieldsStackScreen')
        self.ScreenManager.add_widget(self.FieldsStackScreenControlWidget)
        self.PlayerScreenControlWidget = PlayerScreen(name='PlayerScreen')
        self.ScreenManager.add_widget(self.PlayerScreenControlWidget)

        # Set a convenient way to access the screens
        self.PlayerScreen = self.ScreenManager.get_screen('PlayerScreen')
        self.FilesStackScreen = self.ScreenManager.get_screen('FilesStackScreen')
        self.FilesStackWidget = self.FilesStackScreen.ids.filesstackwidget
        self.FieldsStackScreen = self.ScreenManager.get_screen('FieldsStackScreen')
        self.FieldsStackWidget = self.FieldsStackScreen.ids.fieldsstackwidget

        # Construct the Search Menu
        self.dropdownsearch = DropDown()
        self.btn = Button(text="Current selection", size_hint_y=None, halign="left", height=65, background_color=[0, 0, 0, 0.8], background_normal='')
        self.btn.bind(on_press=self.SelectSearch)
        self.dropdownsearch.add_widget(self.btn)
        for index in self.searches:
            self.btn = Button(text=index['name'], size_hint_y=None, halign="left", height=65, background_color=[0, 0, 0, 0.8], background_normal='')
            self.btn.bind(on_press=self.SelectSearch)
            self.dropdownsearch.add_widget(self.btn)
        self.FilesStackScreen.ids.selectsearch.bind(on_release=self.dropdownsearch.open)
        self.app.search = self.app.searches[0]["search"]
        self.FilesStackScreen.ids.selectsearch.text = self.app.searches[0]["name"]
        # Construct the Select Menu
        self.dropdownselect = DropDown()
        self.btn = Button(text="All", size_hint_y=None, halign="left", height=65, background_color=[0, 0, 0, 0.8], background_normal='')
        self.btn.bind(on_press=self.SelectAll)
        self.dropdownselect.add_widget(self.btn)
        self.btn = Button(text="None", size_hint_y=None,  halign="left", height=65, background_color=[0, 0, 0, 0.8], background_normal='')
        self.btn.bind(on_press=self.SelectNone)
        self.dropdownselect.add_widget(self.btn)
        self.btn = Button(text="Invert", size_hint_y=None, halign="left", height=65, background_color=[0, 0, 0, 0.8], background_normal='')
        self.btn.bind(on_press=self.SelectInvert)
        self.dropdownselect.add_widget(self.btn)
        self.FilesStackScreen.ids.selectfiles.bind(on_release=self.dropdownselect.open)
        self.FilesStackScreen.ids.selectstyle.bind(on_release=self.SelectStyle)
        self.style = 'Thumbnail'
        self.ScreenManager.current = 'FilesStackScreen'

        self.MCWS = MCWS(MCWS_host, MCWS_port)
        self.MCWS.Authenticate()

        if ((self.platform == 'linux') or (self.platform == 'win')):
            Window.size = (550, 700)
            Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
        if (self.platform == 'android'):
            pass
        Window.bind(on_keyboard=self.key_handler)

        return self.ScreenManager


    def key_handler(self, window, keycode1, keycode2, text, modifiers):
        if keycode1 in [27, 1001]:
            if self.ScreenManager.current == 'FieldsStackScreen':
                self.ScreenManager.GotoFilesStackScreen()
            elif self.ScreenManager.current == 'FilesStackScreen':
                App.get_running_app().stop()
            return True
        return False

    def SelectStyle(self, w):
        if self.style == 'Thumbnail':
            self.style = 'Tile'
            self.FilesStackScreen.ids.selectstyle.img.source = join(self.root_dir + "/textures/",  "tile.png")
            self.FilesStackWidget.display_widgets()
        else:
            self.style = 'Thumbnail'
            self.FilesStackScreen.ids.selectstyle.img.source = join(self.root_dir + "/textures/",  "thumbnail.png")
            self.FilesStackWidget.display_widgets()

    def SelectSearch(self, w):
        self.dropdownsearch.select(w.text)
        self.FilesStackScreen.ids.selectsearch.text = w.text
        self.FilesStackWidget.actual_page_number = 0
        if w.text == "Current selection":
            self.search = "Current selection"
            self.app.FilesStackWidget.GetCurrentSelectedFiles()
        for index in self.searches:
            if index["name"] == w.text:
                self.search = index["search"]
                self.app.FilesStackWidget.SearchFiles(self.search)

    def SelectAll(self, w):
        self.dropdownselect.select(w.text)
        self.app.FilesStackWidget.SelectAll()

    def SelectNone(self, w):
        self.dropdownselect.select(w.text)
        self.app.FilesStackWidget.SelectNone()

    def SelectInvert(self, w):
        self.dropdownselect.select(w.text)
        self.app.FilesStackWidget.SelectInvert()

    def build_settings(self, settings):
        settings.register_type('password', SettingPassword)
        settings.add_json_panel("MCWS", self.config, data=self.jsondata)
        settings.bind(on_config_change=self.ConfigChange)

    def ConfigChange(self, a, b, c, d, e):
        self.lang = self.app.config.getdefault("MCWS", "language", "EN")

        self.FieldsStackScreen.TMDB1.lang = self.Languages[self.app.lang]["tmdb"]
        self.DateFormat = self.app.config.getdefault("MCWS", "date", "%d/%m/%Y")
        self.CoverArtMassScrap = self.app.config.getdefault("MCWS", "cover_art", "0")
        self.thumbnail_size = self.app.config.getdefault("MCWS", "thumbnail_size", "Medium")
        self.filesperpage = self.app.config.getdefault("MCWS", "filesperpage", "50")
        if self.MCWS.Token is not None:
            self.ScreenManager.GotoFilesStackScreen()


    def build_config(self, config):
        # Set default configuration
        config.setdefaults("MCWS", {"port": "52199"})
        config.setdefaults("MCWS", {"host": "localhost"})
        config.setdefaults("MCWS", {"admin": "admin"})
        config.setdefaults("MCWS", {"password": "password"})
        config.setdefaults("MCWS", {"language": "EN"})
        config.setdefaults("MCWS", {"thumbnail_size": "Medium"})
        config.setdefaults("MCWS", {"date": "%d/%m/%Y"})
        config.setdefaults("MCWS", {"cover_art": "0"})
        config.setdefaults("MCWS", {"filesperpage": "50"})


if __name__ == '__main__':
    WA = JRScrap2App()
    WA.run()
