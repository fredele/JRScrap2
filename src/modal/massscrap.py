#!/usr/bin/env python
# -*- coding: utf-8 -*-

from kivy.app import App
from kivy.uix.modalview import ModalView
from kivy.properties import ObjectProperty
from threads.massscrap import MassScrapThread


class MassScrap(ModalView):
    lbl = ObjectProperty()

    def __init__(self, **kwargs):
        super(MassScrap, self).__init__(**kwargs)
        self.app = App.get_running_app()
        self.MassScrapThread1 = MassScrapThread(self)

    def on_scrap(self):
        self.MassScrapThread1.start()

    def on_cancel(self):
        self.MassScrapThread1._Thread__stop()
        self.app.FilesStackWidget.SelectNone()
        self.dismiss()
