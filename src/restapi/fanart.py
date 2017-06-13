#!/usr/bin/env python
# -*- coding: utf-8 -*-

from kivy.app import App
from misc.utils import HTTPToSTR
from widgets.thumbnail import ThumbnailWidget
from modal.moviepicker import MoviePicker
from kivy.network.urlrequest import UrlRequest


class FanArt():

    APIkey = '290fc646d21781416de3274019879458'

    def __init__(self, **kwargs):
        self.app = App.get_running_app()

    def Search_Images(self, tmdb_id):
        url = 'http://webservice.fanart.tv/v3/movies/' + tmdb_id + '?api_key=' + self.APIkey
        UrlRequest(url, self.Search_Images_Callback)

    def Search_Images_Callback(self, req, res):
        if 'movieposter' in res:
            view = MoviePicker(auto_dismiss=False)
            view.ids.title.text = 'Posters from FanArt'
            for i in res['movieposter']:
                posterpath = HTTPToSTR(i['url'])
                text = ' '
                Movie = ThumbnailWidget(view, None, text, posterpath)
                # bind the response
                view.ids.stack.add_widget(Movie)
            view.open()

    def Search_Images_TW_Callback(self, req, res):
        resc = []
        if 'movieposter' in res:
            for i in res['movieposter']:
                tab = {}
                tab['source'] = HTTPToSTR(i['url'])
                tab['text'] = ' '
                resc.append(tab)
        self.app.FieldsStackScreen.TW.callback(req, resc)
