from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout

from kivy.clock import Clock

from kivy.graphics import Color

from util import *

from db import DatabaseConnector


class GamesPage(FloatLayout):
	def __init__(self, **kwargs):
		super(GamesPage, self).__init__(**kwargs)
		self.games = []
		Clock.schedule_once(self.load_games, 0)

	def load_games(self, time):
		con = DatabaseConnector()
		self.games = con.get_games()
		for game in self.games:
			self.ids.contentview.content.add_widget(GameCapsule(self.games[game]))


class GameCapsule(BoxLayout):
	def __init__(self, game):
		self.color_dev_status = get_status_color(game.status)
		super(GameCapsule, self).__init__(size_hint=(1, None))
		self.update_ui(game)

	def update_ui(self, game):
		try:
			if game.capsuleimage != '':
				self.ids['capsuleimage'].source = game.capsuleimage
			self.ids['capsuleimage'].reload()
		except:
			pass
		self.ids['status'].text = game.status
		self.ids['version'].text = game.version
		try:
			self.ids['price'].text = str(game.prices['USDS']) + ' USDS'
		except:
			self.ids['price'].text = "Free"


class GamesSearch(FloatLayout):
	pass
