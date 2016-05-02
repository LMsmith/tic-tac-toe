"""utils.py - File for collecting general utility functions."""

import logging
from google.appengine.ext import ndb
import endpoints
import random

def get_by_urlsafe(urlsafe, model):
    """Returns an ndb.Model entity that the urlsafe key points to. Checks
        that the type of entity returned is of the correct kind. Raises an
        error if the key String is malformed or the entity is of the incorrect
        kind
    Args:
        urlsafe: A urlsafe key string
        model: The expected entity kind
    Returns:
        The entity that the urlsafe Key string points to or None if no entity
        exists.
    Raises:
        ValueError:"""
    try:
        key = ndb.Key(urlsafe=urlsafe)
    except TypeError:
        raise endpoints.BadRequestException('Invalid Key')
    except Exception, e:
        if e.__class__.__name__ == 'ProtocolBufferDecodeError':
            raise endpoints.BadRequestException('Invalid Key')
        else:
            raise

    entity = key.get()
    if not entity:
        return None
    if not isinstance(entity, model):
        raise ValueError('Incorrect Kind')
    return entity

def check_win(positions, move):
    """Returns a status string of 'win' or 'continue'
    Args:
        positions: The X's or O's, depending on player turn
        move: The most recent move"""

    status = "continue"
    if move == 1:
        if 2  in positions and 3 in positions:
            status = "win"
        if 4  in positions and 7 in positions:
            status = "win"
        if 5  in positions and 9 in positions:
            status = "win"
    if move == 2:
        if 1  in positions and 3 in positions:
            status = "win"
        if 5  in positions and 8 in positions:
            status = "win"
    if move == 3:
        if 1  in positions and 2 in positions:
            status = "win"
        if 6  in positions and 9 in positions:
            status = "win"
        if 5  in positions and 7 in positions:
            status = "win"
    if move == 4:
        if 5  in positions and 6 in positions:
            status = "win"
        if 1  in positions and 7 in positions:
            status = "win"
    if move == 5:
        if 4  in positions and 6 in positions:
            status = "win"
        if 2  in positions and 8 in positions:
            status = "win"
        if 1  in positions and 9 in positions:
            status = "win"
        if 3  in positions and 7 in positions:
            status = "win"
    if move == 6:
        if 4  in positions and 5 in positions:
            status = "win"
        if 3  in positions and 9 in positions:
            status = "win"
    if move == 7:
        if 8  in positions and 9 in positions:
            status = "win"
        if 1  in positions and 4 in positions:
            status = "win"
        if 3  in positions and 5 in positions:
            status = "win"
    if move == 8:
        if 7  in positions and 9 in positions:
            status = "win"
        if 2  in positions and 5 in positions:
            status = "win"
    if move == 9:
        if 7  in positions and 8 in positions:
            status = "win"
        if 1  in positions and 5 in positions:
            status = "win"
        if 3  in positions and 6 in positions:
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