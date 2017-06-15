#!/usr/bin/env python
# -*- coding: utf-8 -*-

from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.app import App
from widgets.base import BaseWidget


def thumbnail_on_touch_down(self, touch):
    if ((self.ids.movieImage.collide_point(*touch.pos))or(self.stack.collide_point(*touch.pos))):
        if touch.is_double_tap:
            self.app.ScreenManager.GotoFieldsStackScreen()
            self.app.FieldsStackWidget.GetInfo(self.FileKey)


class TilesCheckWidget(BaseWidget):
    movieImage = ObjectProperty()

    def __init__(self, parent_widget, res, **kwargs):
        super(TilesCheckWidget, self).__init__(**kwargs)
        self.app = App.get_running_app()
        self.parent_widget = parent_widget
        self.SetSize(self.app.FilesStackScreen.size_slider.value)
        self.bind(pos=self.update, size=self.update)
        self.bind(on_touch_down=thumbnail_on_touch_down)
        self.FileKey = str(res['Key'])
        self.movieImage.source = self.app.MCWS.address1 + 'File/GetImage?File=' + str(res['Key']) + '&FileType=Key&Type=Thumbnail&ThumbnailSize=' + self.app.thumbnail_size + '&Format=jpg&Token=' + self.app.MCWS.Token
        print(res['Key'])
        self.Update(res)

    def update(self, *args):
        self.width = self.parent_widget.width

    def SetSize(self, val):
        pass

    def SetImage(self, val):
        self.movieImage.source = val

    def SetText(self, val):
        self.ids.movieLabel.text = val

    def Update(self, res):
        if 'Name' in res:
            self.name = res['Name']
            self.ids.movieLabel.text = '[size=24]' + self.name + '[/size]'
        if 'TMDB id' in res:
            self.tmdb_id = res['TMDB id']
        if 'IMDb ID' in res:
            self.imdb_id = res['IMDb ID']
        if 'Description' in res:
            self.movieDescription.text = '\n[b]Description:     [/b]' + res["Description"] + '\n'
        if 'Director' in res:
            self.movieDirector.text = '[b]Director:     [/b]'+res["Director"]
        if 'Actors' in res:
            self.movieActors.text = '[b]Actors:     [/b]'+res["Actors"]+'\n'
