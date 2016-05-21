"""models.py - This file contains the class definitions for the Datastore
entities used by the Game. Because these classes are also regular Python
classes they can include methods (such as 'to_form' and 'new_game')."""

import random
from datetime import date
from protorpc import messages
from google.appengine.ext import ndb


class User(ndb.Model):
    """User profile"""
    name = ndb.StringProperty(required=True)
    email = ndb.StringProperty()
    points = ndb.IntegerProperty(default=0)


class Game(ndb.Model):
    """Game object"""
    remaining_moves = ndb.IntegerProperty(repeated=True)
    x_moves = ndb.IntegerProperty(repeated=True)
    o_moves = ndb.IntegerProperty(repeated=True)
    game_over = ndb.BooleanProperty(required=True, default=False)
    user = ndb.KeyProperty(required=True, kind='User')

    @classmethod
    def new_game(cls, user):
        """Creates and returns a new game"""
        game = Game(user=user,
                    remaining_moves=list(range(1, 10)),
                    x_moves=[],
                    o_moves=[],
                    game_over=False)
        game.put()
        return game

    def to_form(self, message):
        """Returns a GameForm representation of the Game"""
        form = GameForm()
        form.urlsafe_key = self.key.urlsafe()
        form.user_name = self.user.get().name
        form.remaining_moves = self.remaining_moves
        form.x_moves = self.x_moves
        form.o_moves = self.o_moves
        form.game_over = self.game_over
        form.message = message
        return form

    def get_user_games(self, message):
        """Returns active user games"""
        game = GameForm()
        game.user_name = self.user.get().name
        game.urlsafe_key = self.key.urlsafe()
        game.remaining_moves = self.remaining_moves
        game.game_over = self.game_over
        game.message = message
        return game

    def make_move(self, move):
        """Returns a GameForm representation of the Game"""
        if type(move) is not int:
            raise ValueError('Move must be an integer!')

        form = GameForm()
        form.urlsafe_key = self.key.urlsafe()
        form.user_name = self.user.get().name
        form.remaining_moves = self.remaining_moves
        form.x_moves = self.x_moves
        form.o_moves = self.o_moves
        form.game_over = self.game_over
        form.message = message
        return form

    def end_game(self, won=False):
        """Ends the game - if won is True, the player won. - if won is False,
        the player lost."""
        self.game_over = True
        self.put()
        # Add the game to the score 'board'
        score = Score(user=self.user, date=date.today(), won=won,
                                x_moves=self.x_moves, o_moves=self.o_moves)
        score.put()


class Score(ndb.Model):
    """Score object"""
    user = ndb.KeyProperty(required=True, kind='User')
    date = ndb.DateProperty(required=True)
    won = ndb.BooleanProperty(required=True)
    x_moves = ndb.IntegerProperty(repeated=True)
    o_moves = ndb.IntegerProperty(repeated=True)

    def to_form(self):
        return ScoreForm(user_name=self.user.get().name, won=self.won,
                         date=str(self.date), x_moves=self.x_moves, o_moves=
                         self.o_moves)


class GameForm(messages.Message):
    """GameForm for outbound game state information"""
    urlsafe_key = messages.StringField(1, required=True)
    remaining_moves = messages.IntegerField(2, repeated=True)
    x_moves = messages.IntegerField(3, repeated=True)
    o_moves = messages.IntegerField(4, repeated=True)
    game_over = messages.BooleanField(5, required=True)
    message = messages.StringField(6, required=True)
    user_name = messages.StringField(7, required=True)

class Users(messages.Message):
    """Return multiple Users"""
    users = messages.StringField(1, repeated=True)


class GameForms(messages.Message):
    """Return multiple GameForms"""
    items = messages.MessageField(GameForm, 1, repeated=True)

class NewGameForm(messages.Message):
    """Used to create a new game"""
    user_name = messages.StringField(1, required=True)


class MakeMoveForm(messages.Message):
    """Used to make a move in an existing game"""
    move = messages.IntegerField(1, required=True)


class ScoreForm(messages.Message):
    """ScoreForm for outbound Score information"""
    user_name = messages.StringField(1, required=True)
    date = messages.StringField(2, required=True)
    won = messages.BooleanField(3, required=True)
    x_moves = messages.IntegerField(4, repeated=True)
    o_moves = messages.IntegerField(5, repeated=True)


class ScoreForms(messages.Message):
    """Return multiple ScoreForms"""
    items = messages.MessageField(ScoreForm, 1, repeated=True)


class StringMessage(messages.Message):
    """StringMessage-- outbound (single) string message"""
    message = messages.StringField(1, required=True)
