#!/usr/bin/env python
# -*- coding: utf-8 -*-

from kivy.uix.settings import SettingString
from kivy.uix.label import Label


class PasswordLabel(Label):
    pass


class SettingPassword(SettingString):
    def _create_popup(self, instance):
        super(SettingPassword, self)._create_popup(instance)
        self.textinput.password = True

    def add_widget(self, widget, *largs):
        if self.content is None:
            super(SettingString, self).add_widget(widget, *largs)
        if isinstance(widget, PasswordLabel):
            return self.content.add_widget(widget, *largs)
