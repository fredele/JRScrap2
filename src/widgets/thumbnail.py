#!/usr/bin/env python
# -*- coding: utf-8 -*-

from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.app import App
from widgets.base import BaseWidget


def thumbnail_on_touch_down(self, touch):
    if self.ids.movieImage.collide_point(*touch.pos):
        if touch.is_double_tap:
            self.app.ScreenManager.GotoFieldsStackScreen()
            self.app.FieldsStackWidget.GetInfo(self.FileKey)
    if self.ids.movieLabel.collide_point(*touch.pos):
        self.ids.checkbox.active = not self.ids.checkbox.active


class ThumbnailWidget(BaseWidget):
    movieImage = ObjectProperty()
    movieLabel = ObjectProperty()

    def __init__(self, parent_widget, Id, Title, CoverArtURL, **kwargs):
        super(ThumbnailWidget, self).__init__(**kwargs)
        self.app = App.get_running_app()
        self.parent_widget = parent_widget
        self.restid = str(Id)
        self.FileKey = str(Id)
        self.movieLabel.text = Title
        self.movieImage.source = CoverArtURL

    def SetSize(self, val):
        self.width = val
        print(str(val))

    def SetText(self, val):
        self.movieLabel.text = val

    def SetImage(self, val):
        self.movieImage.source = val


class ThumbnailCheckWidget(BaseWidget):
    movieImage = ObjectProperty()
    movieLabel = ObjectProperty()
    checkbox = ObjectProperty()

    def __init__(self, parent_widget, res, **kwargs):
        super(ThumbnailCheckWidget, self).__init__(**kwargs)
        self.app = App.get_running_app()
        self.parent_widget = parent_widget
        self.SetSize(self.app.FilesStackScreen.size_slider.value)
        self.bind(on_touch_down=thumbnail_on_touch_down)
        self.FileKey = str(res['Key'])
        self.Update(res)
        self.movieImage.source = self.app.MCWS.address1 + 'File/GetImage?File='+self.FileKey+'&FileType=Key&Type=Thumbnail&ThumbnailSize='+self.app.thumbnail_size+'&Format=jpg&Token=' + self.app.MCWS.Token

    def SetSize(self, val):
        self.width = val

    def Update(self, res):
                if 'Name' in res:
                    self.name = res['Name']
                    self.ids.movieLabel.text = self.name
                if 'TMDB id' in res:
                    self.tmdb_id = res['TMDB id']
                if 'IMDb ID' in res:
                    self.imdb_id = res['IMDb ID']
                if 'cover_art' in res:
                    if str(self.app.CoverArtMassScrap) == "1":
                        self.movieImage.source = res['cover_art']
                        self.app.MCWS.SetImage(self.FileKey, res['cover_art'])
