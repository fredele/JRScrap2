#!/usr/bin/env python
# -*- coding: utf-8 -*-

from kivy.app import App
from kivy.uix.modalview import ModalView
from kivy.properties import ObjectProperty


class FieldEditer(ModalView):
    textinput = ObjectProperty()
    title = ObjectProperty()

    def __init__(self, obj_src,  **kwargs):
        super(FieldEditer, self).__init__(**kwargs)
        self.app = App.get_running_app()
        self.obj_src = obj_src
        self.title.text = self.obj_src.fieldLabel.text

    def on_cancel(self):
        self.dismiss()

    def on_save(self):
        self.app.MCWS.SetInfo(self.obj_src.Filekey, self.obj_src.fieldLabel.text, self.textinput.text, self.after_save)
        self.dismiss()

    def after_save(self, r, q):
        self.app.MCWS.FileInfo(self.obj_src.Filekey, self.app.FieldsStackWidget.GetInfo_CallBack)

    def Settext(self, value):
        self.textinput.text = value
