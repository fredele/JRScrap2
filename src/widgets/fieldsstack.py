#!/usr/bin/env python
# -*- coding: utf-8 -*-

from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.app import App
from widgets.imagefield import ImageField
from widgets.editfield import EditField
from misc.fields import Movie_Fields
from misc.utils import HTTPToSTR


class FieldsStackWidget(Widget):
    stack = ObjectProperty()

    def __init__(self, **kwargs):
        super(FieldsStackWidget, self).__init__(**kwargs)
        self.app = App.get_running_app()

    def SetWidgetValuebyField(self, key, value):
        r = False
        for widget in self.stack.walk():
            if type(widget) is EditField:
                if widget.fieldLabel.text == key:
                    if widget.SetRESTValue(value):
                        r = True
        return r

    def GetWidgetValuebyField(self, key):
        res = False
        for widget in self.stack.walk():
            if type(widget) is EditField:
                if widget.fieldLabel.text == key:
                    res = widget.valueLabel.text
        if res == '':
            res = False
        return res

    def Clear(self):
        self.stack.clear_widgets()

    def GetInfo(self, key):
        self.Filekey = key
        self.app.MCWS.FileInfo(self.Filekey, self.GetInfo_CallBack)

    def GetInfo_CallBack(self, req, res):
        self.stack.clear_widgets()
        res_dict = self.app.MCWS.MPLToDict2(res)
        self.app.FieldsStackScreen.ids.title.text = res_dict['Name']

        self.imagefield = ImageField(self.Filekey)
        self.imagefield.SetMCImage(self.Filekey)
        self.stack.add_widget(self.imagefield)
        for field in Movie_Fields:
                EditField1 = EditField(self.Filekey)
                self.stack.add_widget(EditField1)
                if field in res_dict:
                    EditField1.SetField(field, value=self.app.MCWS.MCWScorrectdisplay(field, HTTPToSTR(res_dict[field])))
                else:
                    EditField1.SetField(field, "")

    def Save_Fields(self):
        for widget in self.stack.walk():
            if type(widget) is EditField:
                widget.SaveField()
            if type(widget) is ImageField:
                widget.SaveField()

    def Display_res(self, res):
        for widget in self.stack.walk():
            if type(widget) is ImageField:
                if 'cover_art' in res:
                    widget.SetRESTImage(res['cover_art'])
        for field in res:

            self.SetWidgetValuebyField(field, res[field])
