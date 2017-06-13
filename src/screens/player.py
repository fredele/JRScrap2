#!/usr/bin/env python
# -*- coding: utf-8 -*-

from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty

class PlayerScreen(Screen):
	PLAY_STATE = False
	PlayerScreen_cover = ObjectProperty()
	player_slider = ObjectProperty()
	player_artist = ObjectProperty()
	player_album = ObjectProperty()
	player_title = ObjectProperty()
	player_genre = ObjectProperty()
	player_song_elapsed_time = ObjectProperty()
	player_song_total_time = ObjectProperty()
	play_btn = ObjectProperty()

	def __init__(self, **kwargs):
		super(PlayerScreen, self).__init__(**kwargs)

	def on_play_press(self):
		WA.MCWS.PlayPause(WA.MCWS.Status)

	def on_next_press(self):
		WA.MCWS.Next(WA.MCWS.Status)

	def on_previous_press(self):
		WA.MCWS.Previous(WA.MCWS.Status)

	def on_stop_press(self):
		WA.MCWS.Stop(WA.MCWS.Status)
