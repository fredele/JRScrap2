#!/usr/bin/env python
# -*- coding: utf-8 -*-

from kivy.app import App
from kivy.uix.modalview import ModalView
from kivy.properties import ObjectProperty
from misc.utils import STRToHTTP


class FilesSearch(ModalView):
    textinput = ObjectProperty()
    title = ObjectProperty()

    def __init__(self, obj_src,  **kwargs):
        super(FilesSearch, self).__init__(**kwargs)
        self.app = App.get_running_app()
        self.obj_src = obj_src

    def on_cancel(self):
        self.dismiss()

    def on_search(self):
        query = '[Media%20Type]=[Video]%20[Media%20Sub%20Type]=[Movie]%20~sort=[Name]%20[Name]="' + STRToHTTP(self.textinput.text) + '"&Fields=Name,Key,TMDB%20id,IMDb%20ID,Date,Description,Director,Actors,Keywords'
        self.app.FilesStackScreen.ids.selectsearch.text = "Search results"
        self.app.FilesStackWidget.SearchFiles(query)
        self.dismiss()
