#Tic-Tac-Toe: Full Stack Nanodegree Project 4 Refresh

## Set-Up Instructions:
1.  Update the value of application in app.yaml to the app ID you have registered
 in the App Engine admin console and would like to use to host your instance of this sample.
1.  Run the app with the devserver using dev_appserver.py DIR, and ensure it's
 running by visiting the API Explorer - by default localhost:8080/_ah/api/explorer.
1.  (Optional) Generate your client library(ies) with the endpoints tool.
 Deploy your application.
 
 
 
##Game Description:
Tic-Tac-Toe is a classic 2 player game played on a board with 9 spaces. In this version, the player makes a move by choosing the corresponding number on the board below.

                                                   1 | 2 | 3
                                                  ___ ___ ___
                                                   4 | 5 | 6
                                                  ___ ___ ___
                                                   7 | 8 | 9

Players take turns marking spaces (one player plays as 'X' and the other plays as 'O'). The game is won when one player has marked 3 spaces in a row horizontally, vertically or diagonally.  If all spaces are filled and neither player has won, the game ends in a draw.

Many different Tic-Tac-Toe games can be played by many different Users at any
given time. Each game can be retrieved or played by using the path parameter
`urlsafe_game_key`.

Players earn 1 point per tie and 2 points per win.

##Files Included:
 - api.py: Contains endpoints and game playing logic.
 - app.yaml: App configuration.
 - cron.yaml: Cronjob configuration.
 - main.py: Handler for taskqueue handler.
 - models.py: Entity and message definitions including helper methods.
 - utils.py: Helper function for retrieving ndb.Models by urlsafe Key string. Also contains game logic for computer moves and determining a winner.

##Endpoints Included:
 - **create_user**
    - Path: 'user'
    - Method: POST
    - Parameters: user_name, email (optional)
    - Returns: Message confirming creation of the User.
    - Description: Creates a new User. user_name provided must be unique. Will 
    raise a ConflictException if a User with that user_name already exists.
    
 - **new_game**
    - Path: 'game'
    - Method: POST
    - Parameters: user_name, remaining_moves, x_moves, o_moves, game_over
    - Returns: GameForm with initial game state.
    - Description: Creates a new Game. user_name provided must correspond to an
    existing user - will raise a NotFoundException if not. Returns a urlsafe_game_key identifying the game.
     
 - **get_game**
    - Path: 'game/{urlsafe_game_key}'
    - Method: GET
    - Parameters: urlsafe_game_key
    - Returns: GameForm with current game state.
    - Description: Returns the current state of a game.
    
 - **cancel_game**
    - Path: 'game/{urlsafe_game_key}'
    - Method: DELETE
    - Parameters: urlsafe_game_key
    - Returns: StringMessage confirming game cancellation.
    - Description: Cancels an open game.

 - **make_move**
    - Path: 'game/{urlsafe_game_key}'
    - Method: PUT
    - Parameters: urlsafe_game_key, move
    - Returns: GameForm with new game state.
    - Description: Accepts a 'move' and returns the updated state of the game.
    If this causes a game to end, a corresponding Score entity will be created and the User's point total will be incremented if points were earned.
    
 - **get_game_history**
    - Path: 'scores'
    - Method: GET
    - Parameters: None
    - Returns: ScoreForms.
    - Description: Returns all completed games in the database (unordered).
    
 - **get_user_games**
    - Path: 'scores/user/{user_name}'
    - Method: GET
    - Parameters: user_name
    - Returns: ScoreForms. 
    - Description: Returns all active games recorded by the provided player (unordered).
    Will raise a NotFoundException if the User does not exist.

 - **get_user_rankings**
    - Path: 'users/rankings'
    - Method: GET
    - Parameters: None
    - Returns: Users. 
    - Description: Returns all Users who have earned points in games, ordered by highest points total.

##Models Included:
 - **User**
    - Stores unique user_name and (optional) email address.
    
 - **Game**
    - Stores unique game states. Associated with User model via KeyProperty.
    
 - **Score**
    - Records completed games. Associated with Users model via KeyProperty.
    
##Forms Included:
 - **GameForm**
    - Representation of a Game's state (urlsafe_key, attempts_remaining,
    game_over flag, message, user_name).
 - **NewGameForm**
    - Used to create a new game (user_name, remaining_moves, x_moves, o_moves, game_over)
 - **MakeMoveForm**
    - Inbound make move form (move).
 - **ScoreForm**
    - Representation of a completed game's Score (user_name, date, won flag).
 - **ScoreForms**
    - Multiple ScoreForm container.
 - **StringMessage**
    - General purpose String container.
