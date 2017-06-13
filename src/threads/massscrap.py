#!/usr/bin/env python
# -*- coding: utf-8 -*-

from threading import Thread
from kivy.app import App
from restapi.tmdb import TMDB

exitFlag = 0


class MassScrapThread(Thread):
    def __init__(self, view):  # view is the modal.massscrap view
        Thread.__init__(self)
        self.view = view
        self.app = App.get_running_app()
        self.files = self.app.FilesStackWidget.GetCheckedWidgetsInfos()
        if len(self.files) > 0:
            self.view.lbl.text = 'Nbr. of files to scrap : ' + str(len(self.files))
        else:
            self.view.lbl.text = "Please, check some files first."
        self.index = 0
        self.TMDB2 = TMDB()

    def GetIndex(self):

        if self.index < len(self.files):
            print("Srcapping ...")
            self.view.lbl.text = "Get :" + self.files[self.index]['name'] + '   (' + str(self.index+1) + '/' + str(len(self.files))+')'
            if ((self.files[self.index]['imdb id'] is not None) and (self.files[self.index]['tmdb id'] is not None)):
                self.TMDB2.Search_TMDB_ID(self.files[self.index]['tmdb id'], self.TMDB2.Search_TMDB_ID_MASS_Callback)
            if ((self.files[self.index]['imdb id'] is None) and (self.files[self.index]['tmdb id'] is not None)):
                self.TMDB2.Search_TMDB_ID(self.files[self.index]['tmdb id'], self.TMDB2.Search_TMDB_ID_MASS_Callback)
            if ((self.files[self.index]['imdb id'] is not None) and (self.files[self.index]['tmdb id'] is None)):
                self.TMDB2.Search_IMDB_ID(self.files[self.index]['imdb id'], self.TMDB2.Search_IMDB_ID_MASS_Callback)
            if ((self.files[self.index]['imdb id'] is None) and (self.files[self.index]['tmdb id'] is None)):
                # Skip this file
                self.index += 1
                self.GetIndex()
            self.index += 1
        else:
            self.view.lbl.text = ""
            self.view.on_cancel()

    def run(self):
        self.GetIndex()

    def GetFileKeybyTMDB_ID(self, tmdb):
        r = ''
        for item in self.files:
            if item['tmdb id'] == tmdb:
                r = item['key']
        return r

    def SetTMDB_IDbyIMDB_ID(self, imdb, tmdb):
        for item in self.files:
            if item['imdb id'] == imdb:
                item['tmdb id'] = tmdb
