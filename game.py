"""game.py - File for collecting game functions."""

import logging
from google.appengine.ext import ndb
import endpoints
import random

def check_win(positions, move):
    """Returns a status string of 'win' or 'continue'
    Args:
        positions: The X's or O's, depending on player turn
        move: The most recent move"""

    status = "continue"
    winning_moves = [
        [1,2,3],
        [1,4,7],
        [1,5,9],
        [2,5,8],
        [3,5,7],
        [3,6,9],
        [4,5,6],
        [7,8,9]
    ]
    for winning_move in winning_moves:
        if set(winning_move) < set(sorted(positions)):
            status = "win"

    return status

def computer_move(omoves, xmoves, remaining):
    """Returns the computer's move
    Args:
        omoves: The O's already marked
        xmoves: The X's already marked
        remaining: The remaining empty spaces"""

    choice = random.choice(remaining)

    """If the middle space is available and no winning or
        saving moves are available, computer chooses 5"""
    if 5 in remaining:
        choice = 5

    player_moves = [xmoves, omoves]

    """Check if there is a move to prevent user from winning
        or to allow computer to win. Prioritize winning over
        saving"""
    for moves in player_moves:
        if 1 in moves:
            if 2 in moves and 3 in remaining:
                choice = 3
            if 3 in moves and 2 in remaining:
                choice = 2
            if 4 in moves and 7 in remaining:
                choice = 7
            if 5 in moves and 9 in remaining:
                choice = 9
            if 7 in moves and 4 in remaining:
                choice = 4
            if 9 in moves and 5 in remaining:
                choice = 5
        if 2 in moves:
            if 3 in moves and 1 in remaining:
                choice = 1
            if 5 in moves and 8 in remaining:
                choice = 8
            if 8 in moves and 5 in remaining:
                choice = 5
        if 3 in moves:
            if 5 in moves and 7 in remaining:
                choice = 7
            if 6 in moves and 9 in remaining:
                choice = 9
            if 7 in moves and 5 in remaining:
                choice = 5
            if 9 in moves and 6 in remaining:
                choice = 6
        if 4 in moves:
            if 5 in moves and 6 in remaining:
                choice = 6
            if 6 in moves and 5 in remaining:
                choice = 5
            if 7 in moves and 1 in remaining:
                choice = 1
        if 5 in moves:
            if 6 in moves and 4 in remaining:
                choice = 4
            if 7 in moves and 3 in remaining:
                choice = 3
            if 8 in moves and 2 in remaining:
                choice = 2
            if 9 in moves and 1 in remaining:
                choice = 1
        if 6 in moves:
            if 9 in moves and 3 in remaining:
                choice = 3
        if 7 in moves:
            if 8 in moves and 9 in remaining:
                choice = 9
            if 9 in moves and 8 in remaining:
                choice = 8
        if 8 in moves:
            if 9 in moves and 7 in remaining:
                choice = 7

    return choice