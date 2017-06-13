#!/usr/bin/env python
# -*- coding: utf-8 -*-

from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from kivy.app import App
from modal.massscrap import MassScrap


class FilesStackScreen(Screen):
    size_slider = ObjectProperty()
    filesstackwidget = ObjectProperty()
    lowerbox = ObjectProperty()

    def __init__(self, **kwargs):
        super(FilesStackScreen, self).__init__(**kwargs)
        self.app = App.get_running_app()

    def on_size_slide(self):
        self.filesstackwidget.SetWidgetsSize(int(self.size_slider.value))

    def on_slide_up(self):
        self.app.store.put(self.app.style+"Zoom", value=self.size_slider.value)

    def MassScrap(self):
        self.MassScrapView = MassScrap()
        self.MassScrapView.open()
