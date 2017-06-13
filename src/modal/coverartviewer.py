#!/usr/bin/env python
# -*- coding: utf-8 -*-

from kivy.app import App
from kivy.uix.modalview import ModalView
from kivy.properties import ObjectProperty


class CoverArtViewer(ModalView):
    im = ObjectProperty()


    def __init__(self, **kwargs):
        super(CoverArtViewer, self).__init__(**kwargs)
        self.app = App.get_running_app()

    def SetImage(self, url):
        self.im.source = url

    def on_close(self):
        self.dismiss()
