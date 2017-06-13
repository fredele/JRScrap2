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
        search = self.app.searches[0]["search"]
        self.app.FilesStackWidget.SearchFiles(search)

    def GotoFieldsStackScreen(self):
        self.current = 'FieldsStackScreen'
        self.app.FieldsStackWidget.Clear()


class WindowApp(App):
    Schedule_time = 1

    def __init__(self):
        super(WindowApp, self).__init__()
        self.platform = utils.platform
        Logger.debug('PLATEFORM : ' + self.platform)
        if ((self.platform == 'linux') or (self.platform == 'windows')):
            Window.size = (550, 700)
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
        MCWS_host = self.config.getdefault("MCWS", "host", "127.0.0.1")
        self.filesperpage = self.config.getdefault("MCWS", "filesperpage", "10")
        self.MCWS = MCWS(MCWS_host, MCWS_port)

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
        self.current = 'FilesStackScreen'

        self.MCWS.Authenticate()

        return self.ScreenManager

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
        if w.text == "Current selection":
            self.app.FilesStackWidget.GetCurrentSelectedFiles()
        for index in self.searches:
            if index["name"] == w.text:
                search = index["search"]
                self.app.FilesStackWidget.SearchFiles(search)

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
        self.filesperpage = self.app.config.getdefault("MCWS", "filesperpage", "10")
        if self.MCWS.Token is not None:
            self.ScreenManager.GotoFilesStackScreen()


    def build_config(self, config):
        # Set default configuration
        config.setdefaults("MCWS", {"port": "52199"})
        config.setdefaults("MCWS", {"host": "127.0.0.1"})
        config.setdefaults("MCWS", {"admin": "admin"})
        config.setdefaults("MCWS", {"password": "password"})
        config.setdefaults("MCWS", {"language": "EN"})
        config.setdefaults("MCWS", {"thumbnail_size": "Medium"})
        config.setdefaults("MCWS", {"date": "%d/%m/%Y"})
        config.setdefaults("MCWS", {"cover_art": "0"})
        config.setdefaults("MCWS", {"filesperpage": "10"})


if __name__ == '__main__':
    WA = WindowApp()
    WA.run()
