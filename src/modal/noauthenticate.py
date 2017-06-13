#!/usr/bin/env python
# -*- coding: utf-8 -*-

from kivy.app import App
from kivy.uix.modalview import ModalView
from kivy.properties import ObjectProperty
from threads.massscrap import MassScrapThread


class NoConnection(ModalView):
    lbl = ObjectProperty()

    def __init__(self, **kwargs):
        super(NoConnection, self).__init__(**kwargs)
        self.app = App.get_running_app()

    def on_cancel(self):
        self.dismiss()
