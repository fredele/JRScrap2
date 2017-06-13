#!/usr/bin/env python
# -*- coding: utf-8 -*-

from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.app import App
from kivy.uix.textinput import TextInput
from modal.fieldediter import FieldEditer


class EditField(Widget):
    fieldLabel = ObjectProperty()
    valueLabel = ObjectProperty()

    def __init__(self, Filekey, **kwargs):
        super(EditField, self).__init__(**kwargs)
        self.app = App.get_running_app()
        self.Filekey = Filekey
        self.DisplayMCValue = True
        self.RESTvalue = None
        self.editing = False

    def SaveField(self):
        if self.DisplayMCValue is False:
            self.app.MCWS.SetInfo(self.Filekey, self.fieldLabel.text, self.RESTvalue, self.Save_Field_callback)

    def Save_Field_callback(self, req, res):
            print('Save_Field')
            self.valueLabel.text = self.RESTvalue
            self.DisplayMCValue = True
            self.RESTvalue = None

    def Save_Field_callback_Error(self, req, res):
            print(res)

    def SetField(self, field, value):
        self.fieldLabel.text = str(field)
        self.valueLabel.text = str(value)
        self.MCvalue = str(value)

    def SetRESTValue(self, value):
        r = False
        if((value != self.valueLabel.text) and (value is not None)and (value is not None)):
            self.RESTvalue = value
            self.valueLabel.text = '[b]' + value + '[/b]'
            self.DisplayMCValue = False
            r = True
        return r

    def on_enter(self, src_obj):
        self.valueLabel.text = src_obj.text
        self.ids.valueLabel.clear_widgets()
        self.editing = False

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if self.RESTvalue is not None:
                if self.DisplayMCValue is False:
                    self.DisplayMCValue = True
                    self.valueLabel.text = self.MCvalue
                else:
                    self.DisplayMCValue = False
                    self.valueLabel.text = '[b]' + self.RESTvalue + '[/b]'
            if touch.is_double_tap:
                if self.editing is False:

                    FieldEditer1 = FieldEditer(self, auto_dismiss=False)
                    if self.DisplayMCValue is True:
                        FieldEditer1.Settext(self.valueLabel.text)
                    else:
                        FieldEditer1.Settext(self.RESTvalue)

                    FieldEditer1.open()
