from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout

from kivy.clock import Clock

from .storepage import StorePage
from .gamespage import GameCapsule

from data import Game

from main import ConfirmPopup

from db import DatabaseConnector
from util import *


class PublishPage(FloatLayout):
	def __init__(self, **kwargs):
		super(PublishPage, self).__init__(**kwargs)
		self.games = []
		Clock.schedule_once(self.load_games, 0)

	def load_games(self, time):
		con = DatabaseConnector("bolt://10.0.0.3:7687", "Gaerax", "password")
		self.games = con.get_games()
		con.close()
		for game in self.games:
			self.ids.contentview.content.add_widget(GamePublishEdit(self.games[game]))

	def create_game(self):
		self.ids.contentview.content.add_widget(GamePublishEdit())


class GamePublishEdit(BoxLayout):
	def __init__(self, game=None):
		super(GamePublishEdit, self).__init__(size_hint=(1, None))
		self.orientation = "vertical"
		if game is None:
			self.game = Game()
			self.editdisabled = False
		else:
			self.game = game
			self.editdisabled = True
		self.old_game = self.game
		Clock.schedule_once(self.publish_edit_update_ui, 0)

		self.revert()

		self.previewCapsule = GameCapsule(self.game)
		self.previewCapsule.pos_hint = {'x': 0, 'y': 0}
		self.ids.capsulecontainer.add_widget(self.previewCapsule)

	def publish_edit_update_ui(self, delay=0):
		self.ids.title.disabled = self.editdisabled
		self.ids.description.disabled = self.editdisabled
		self.ids.longdescription.disabled = self.editdisabled
		self.ids.author.disabled = self.editdisabled
		# self.ids.author.disabled = True # Author name shouldn't be changed, because they will lose access
		self.ids.capsuleimage.disabled = self.editdisabled
		self.ids.tags.disabled = self.editdisabled
		self.ids.version.disabled = self.editdisabled
		self.ids.trailer.disabled = self.editdisabled
		self.ids.screenshots.disabled = self.editdisabled
		self.ids.prices.disabled = self.editdisabled
		self.ids.downloads.disabled = self.editdisabled
		self.ids.executables.disabled = self.editdisabled
		self.ids.paymentaddress.disabled = self.editdisabled
		self.ids.status.disabled = self.editdisabled
		if self.editdisabled:
			self.ids.publishbutton.text = 'Edit'
		else:
			self.ids.publishbutton.text = 'Publish'

	def publish_edit(self):
		if self.editdisabled:
			pass # start edit
		else:
			self.update_game()
			self.old_game = self.game
			con = DatabaseConnector("bolt://10.0.0.3:7687", "Gaerax", "password")
			con.publish_game(self.game)
			con.close()
			# warning = ConfirmPublishPopup(self.game)
			# warning.open()

		self.editdisabled = not self.editdisabled # start edit
		self.publish_edit_update_ui()

	def update_game(self, delay=0):
		self.game.title = self.ids['title'].text
		self.game.description = self.ids['description'].text
		self.game.longdescription = self.ids['longdescription'].text
		self.game.author = self.ids['author'].text
		self.game.capsuleimage = self.ids['capsuleimage'].text
		self.game.tags = csv_to_list(self.ids['tags'].text)
		self.game.status = self.ids['status'].text
		self.game.version = self.ids['version'].text
		self.game.trailer = self.ids['trailer'].text
		self.game.screenshots = csv_to_list(self.ids['screenshots'].text)
		self.game.prices = string_to_object(self.ids['prices'].text)
		self.game.downloads = string_to_object(self.ids['downloads'].text)
		self.game.executables = string_to_object(self.ids['executables'].text)
		self.game.paymentaddress = self.ids['paymentaddress'].text
		self.previewCapsule.update_ui(self.game)


	def revert(self):
		self.game = self.old_game
		self.ids['title'].text = self.game.title
		self.ids['description'].text = self.game.description
		self.ids['longdescription'].text = self.game.longdescription
		self.ids['author'].text = self.game.author
		self.ids['capsuleimage'].text = self.game.capsuleimage
		self.ids['tags'].text = list_to_csv(self.game.tags)
		self.ids['status'].text = self.game.status
		self.ids['version'].text = self.game.version
		self.ids['trailer'].text = self.game.trailer
		self.ids['screenshots'].text = list_to_csv(self.game.screenshots)
		self.ids['prices'].text = str(self.game.prices)
		self.ids['downloads'].text = str(self.game.downloads)
		self.ids['executables'].text = str(self.game.executables)
		self.ids['paymentaddress'].text = self.game.paymentaddress


	def show_store(self):
		page = StorePage(self.game)
		page.open()


class ConfirmPublishPopup(ConfirmPopup):
	def __init__(self, game):
		super(ConfirmPublishPopup, self).__init__()
		self.game = game

	def on_ok(self):
		con = DatabaseConnector("bolt://10.0.0.3:7687", "Gaerax", "password")
		con.publish_game(self.game)
		con.close()

	def on_cancel(self):
		pass