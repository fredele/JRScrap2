#!/usr/bin/env python
# -*- coding: utf-8 -*-

from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.app import App
from modal.coverartviewer import CoverArtViewer

class ImageField(Widget):
    srcImage = ObjectProperty()
    srcLabel = ObjectProperty()

    def __init__(self, Filekey, **kwargs):
        self.Filekey = Filekey
        super(ImageField, self).__init__(**kwargs)
        self.app = App.get_running_app()
        self.DisplayMCValue = True
        self.color = 'ff3333'
        self.RESTImageURL = None
        self.app = App.get_running_app()

    def SetMCImage(self, Filekey):
        self.Filekey = Filekey
        self.MCImageURL = self.app.MCWS.address1 + 'File/GetImage?File=' + self.Filekey + '&FileType=Thumbnail&ThumbnailSize='+self.app.thumbnail_size+'&Token=' + self.app.MCWS.Token
        print(self.MCImageURL)
        try:
            self.srcImage.source = self.MCImageURL
        except (RuntimeError, TypeError, NameError):
            pass

    def SetRESTImage(self, imageURL):
        self.RESTImageURL = imageURL
        try:
            self.srcImage.source = self.RESTImageURL
        except (RuntimeError, TypeError, NameError):
            pass
        self.DisplayMCValue = False

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if self.RESTImageURL is not None:
                if self.DisplayMCValue is False:
                    self.DisplayMCValue = True
                    self.srcImage.source = self.MCImageURL
                else:
                    self.DisplayMCValue = False
                    self.srcImage.source = self.RESTImageURL
            if touch.is_double_tap:
                view = CoverArtViewer()
                try:
                    view.SetImage(self.app.MCWS.address1 + 'File/GetImage?File=' + self.Filekey + '&FileType=Key&Type=Full&Format=jpg&Token=' + self.app.MCWS.Token)
                except (RuntimeError, TypeError, NameError):
                    pass
                view.open()

    def SaveField(self):
        if ((self.RESTImageURL is not None) and (self.DisplayMCValue is False)):
            self.app.MCWS.SetImage(self.Filekey, self.RESTImageURL)
