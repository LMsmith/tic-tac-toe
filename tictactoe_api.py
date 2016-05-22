# -*- coding: utf-8 -*-`
"""tictactoe_api.py - Create and configure the Game API exposing the
resources. This can also contain game logic. For more complex games it would
be wise to move game logic to another file. Ideally the API will be simple,
concerned primarily with communication to/from the API's users."""


import endpoints
from protorpc import remote, messages
from google.appengine.ext import ndb

from models import User, Game, Score, Users
from models import StringMessage, NewGameForm, GameForm, MakeMoveForm,\
    ScoreForms, GameForms
from utils import get_by_urlsafe
from utils import check_win
from utils import computer_move

NEW_GAME_REQUEST = endpoints.ResourceContainer(NewGameForm)
GET_GAME_REQUEST = endpoints.ResourceContainer(
        urlsafe_game_key=messages.StringField(1),)
DELETE_GAME_REQUEST = endpoints.ResourceContainer(
        urlsafe_game_key=messages.StringField(1),)
MAKE_MOVE_REQUEST = endpoints.ResourceContainer(
    MakeMoveForm,
    urlsafe_game_key=messages.StringField(1),)
USER_REQUEST = endpoints.ResourceContainer(user_name=messages.StringField(1),
                                           email=messages.StringField(2))


@endpoints.api(name='tic_tac_toe', version='v1')
class TicTacToeApi(remote.Service):
    """Game API"""
    @endpoints.method(request_message=USER_REQUEST,
                      response_message=StringMessage,
                      path='user',
                      name='create_user',
                      http_method='POST')
    def create_user(self, request):
        """Create a User. Requires a unique username"""
        if User.query(User.name == request.user_name).get():
            raise endpoints.ConflictException(
                    'A User with that name already exists!')
        if request.email:
            user = User(name=request.user_name, email=request.email)
        else:
            user = User(name=request.user_name)
        user.put()
        return StringMessage(message='User {} created!'.format(
                request.user_name))

    @endpoints.method(request_message=NEW_GAME_REQUEST,
                      response_message=GameForm,
                      path='game',
                      name='new_game',
                      http_method='POST')
    def new_game(self, request):
        """Creates new game"""
        user = User.query(User.name == request.user_name).get()
        if not user:
            raise endpoints.NotFoundException(
                    'A User with the name {} does not exist!'
                    .format(request.user_name))

        game = Game.new_game(user.key)

        # Use a task queue to update the average attempts remaining.
        # This operation is not needed to complete the creation of a new game
        # so it is performed out of sequence.
        # taskqueue.add(url='/tasks/cache_average_attempts')
        return game.to_form('Good luck playing Tic-Tac-Toe!')

    @endpoints.method(request_message=GET_GAME_REQUEST,
                      response_message=GameForm,
                      path='game/{urlsafe_game_key}',
                      name='get_game',
                      http_method='GET')
    def get_game(self, request):
        """Return the current game state."""
        game = get_by_urlsafe(request.urlsafe_game_key, Game)
        if game:
            return game.to_form('Time to make a move!')
        else:
            raise endpoints.NotFoundException('Game not found!')

    @endpoints.method(request_message=DELETE_GAME_REQUEST,
                      response_message=StringMessage,
                      path='game/{urlsafe_game_key}',
                      name='cancel_game',
                      http_method='DELETE')
    def cancel_game(self, request):
        """Cancels a current game."""
        game = get_by_urlsafe(request.urlsafe_game_key, Game)
        if game:
            if game.game_over:
                raise endpoints.ConflictException(
                        'Game is already completed!')
            key = ndb.Key(urlsafe=request.urlsafe_game_key)
            key.delete()
            return StringMessage(message='Game cancelled!')
        else:
            raise endpoints.NotFoundException('Game not found!')

    @endpoints.method(request_message=MAKE_MOVE_REQUEST,
                      response_message=GameForm,
                      path='game/{urlsafe_game_key}',
                      name='make_move',
                      http_method='PUT')
    def make_move(self, request):
        """Makes a move. Returns a game state with message"""
        game = get_by_urlsafe(request.urlsafe_game_key, Game)
        user = User.query(User.key == game.user).get()
        allowed_moves = list(range(1, 10))

        if request.move not in allowed_moves:
            return game.to_form('Move must be between 1 and 9!')

        if game.game_over:
            return game.to_form('Game already over!')

        if request.move not in game.remaining_moves:
            return game.to_form('That spot is already marked!')

        game.remaining_moves.remove(request.move)
        game.x_moves.append(request.move)
        msg = "'X' marked on {}".format(request.move)

        is_player_win = check_win(game.x_moves, request.move)

        if is_player_win == "win":
            game.end_game(True)
            user.points += 2
            user.put()
            return game.to_form("Player wins!")

        if(len(game.remaining_moves) == 0):
            user.points += 1
            user.put()
            game.end_game(True)
            return game.to_form("The game has ended in a tie!")

        omove = computer_move(game.o_moves, game.x_moves,
                              game.remaining_moves)
        game.remaining_moves.remove(omove)
        game.o_moves.append(omove)
        is_computer_win = check_win(game.o_moves, omove)

        if is_computer_win == "win":
            user.name += 2
            game.end_game(True)
            return game.to_form("Computer wins!")

        msg += ", 'O' marked on {}".format(omove)

        game.put()
        return game.to_form(msg)

    @endpoints.method(response_message=ScoreForms,
                      path='scores',
                      name='get_game_history',
                      http_method='GET')
    def get_game_history(self, request):
        """Return all scores"""
        return ScoreForms(items=[score.to_form() for score in Score.query()])

    @endpoints.method(request_message=USER_REQUEST,
                      response_message=GameForms,
                      path='scores/user/{user_name}',
                      name='get_user_games',
                      http_method='GET')
    def get_user_games(self, request):
        """Returns all of an individual User's games"""
        user = User.query(User.name == request.user_name).get()
        if not user:
            raise endpoints.NotFoundException(
                    'A User with that name does not exist!')
        games = Game.query(ndb.AND(Game.user == user.key,
                           ndb.AND(if Game.game_over False)))

        return GameForms(items=[game.get_user_games('user games')
                         for game in games])

    @endpoints.method(response_message=Users,
                      path='users/rankings',
                      name='get_user_rankings',
                      http_method='GET')
    def get_user_rankings(self, request):
        """Return all users"""
        users = User.query().order(-User.points)
        return Users(users=[(user.name + ' : ' +
                     str(user.points) + ' points') for user in users])


api = endpoints.api_server([TicTacToeApi])