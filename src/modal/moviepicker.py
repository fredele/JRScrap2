#!/usr/bin/env python
# -*- coding: utf-8 -*-

from kivy.uix.modalview import ModalView
from kivy.app import App


class MoviePicker(ModalView):
    def __init__(self, **kwargs):
        super(MoviePicker, self).__init__(**kwargs)
        self.app = App.get_running_app()

    def on_close(self):
        self.dismiss()
