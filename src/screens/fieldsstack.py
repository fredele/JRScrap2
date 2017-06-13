#!/usr/bin/env python
# -*- coding: utf-8 -*-

from kivy.uix.screenmanager import Screen
from kivy.app import App
from restapi.tmdb import TMDB
from restapi.fanart import FanArt
from threads import threadworker
from modal.moviepicker import MoviePicker
from widgets.thumbnail import ThumbnailWidget


def ThumbnailWidget_on_touch_down(instance, touch):
    if instance.collide_point(*touch.pos):
        instance.parent_widget.on_close()
        instance.app.MCWS.SetImage(instance.app.FieldsStackWidget.Filekey, instance.movieImage.source)


class FieldsStackScreen(Screen):
    def __init__(self, **kwargs):
        super(FieldsStackScreen, self).__init__(**kwargs)
        self.app = App.get_running_app()

        # Create all the API's here ..
        self.TMDB1 = TMDB()
        self.FanArt1 = FanArt()

        # Threadworkers
        self.TW = threadworker.ThreadWorker(self.SearchAllImages_Callback)


# TMDB Section:
# -------------

    def TMDBSearch(self):
        if ((self.app.FieldsStackWidget.GetWidgetValuebyField('IMDb ID') is not False) and (self.app.FieldsStackWidget.GetWidgetValuebyField('TMDB id') is False)):
            self.TMDB1.Search_IMDB_ID(self.app.FieldsStackWidget.GetWidgetValuebyField('IMDb ID'), self.TMDB1.Search_IMDB_ID_Callback)
        if ((self.app.FieldsStackWidget.GetWidgetValuebyField('IMDb ID') is False) and (self.app.FieldsStackWidget.GetWidgetValuebyField('TMDB id') is not False)):
            self.TMDB1.Search_TMDB_ID(self.app.FieldsStackWidget.GetWidgetValuebyField('TMDB id'), self.TMDB1.Search_TMDB_ID_Callback)
        if ((self.app.FieldsStackWidget.GetWidgetValuebyField('IMDb ID') is not False) and (self.app.FieldsStackWidget.GetWidgetValuebyField('TMDB id') is not False)):
            self.TMDB1.Search_TMDB_ID(self.app.FieldsStackWidget.GetWidgetValuebyField('TMDB id'), self.TMDB1.Search_TMDB_ID_Callback)
        if ((self.app.FieldsStackWidget.GetWidgetValuebyField('IMDb ID') is False) and (self.app.FieldsStackWidget.GetWidgetValuebyField('TMDB id') is False)):
            self.TMDB1.Search_Movies_Name(self.app.FieldsStackWidget.GetWidgetValuebyField('Name'))

    def TMDBSearchImages(self):
        if self.app.FieldsStackWidget.GetWidgetValuebyField('TMDB id') is not False:
            self.TMDB1.Search_Images(self.app.FieldsStackWidget.GetWidgetValuebyField('TMDB id'))

    def FanArtSearchImages(self):
        if self.app.FieldsStackWidget.GetWidgetValuebyField('TMDB id') is not False:
            self.FanArt1.Search_Images(self.app.FieldsStackWidget.GetWidgetValuebyField('TMDB id'))

    def SearchAllImages(self):
        imdb_id = self.app.FieldsStackWidget.GetWidgetValuebyField('IMDb ID')
        tmdb_id = self.app.FieldsStackWidget.GetWidgetValuebyField('TMDB id')
        if tmdb_id is not False:
            self.TW.AddThread('tmdb', 'https://api.themoviedb.org/3/movie/' + tmdb_id + '/images?api_key=' + self.TMDB1.APIkey + self.TMDB1.lang, self.TMDB1.Search_Images_TW_Callback)
        if imdb_id is not False:
            self.TW.AddThread('fanart', 'http://webservice.fanart.tv/v3/movies/' + imdb_id + '?api_key=' + self.FanArt1.APIkey,                 self.FanArt1.Search_Images_TW_Callback)
        self.TW.Runthreads()

    def SearchAllImages_Callback(self, res):
        view = MoviePicker(auto_dismiss=False)
        view.ids.title.text = 'Cover'
        for api in res:
            for i in api['result']:
                Movie = ThumbnailWidget(view, None, i['text'], i['source'])
                print("adding ...")
                view.ids.stack.add_widget(Movie)
                Movie.bind(on_touch_down=ThumbnailWidget_on_touch_down)
        view.open()
