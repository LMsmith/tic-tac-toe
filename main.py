#!/usr/bin/env python

"""main.py - This file contains handlers that are called by taskqueue and/or
cronjobs."""
import logging

import webapp2
from google.appengine.api import mail, app_identity
from api import TicTacToeApi

from models import User
from models import Game


class SendReminderEmail(webapp2.RequestHandler):
    def get(self):
        """Send a reminder email to each User involved in an open game.
        Called every hour using a cron job"""
        app_id = app_identity.get_application_id()
        users = User.query(if User.email not None)
        games = Game.query(if Game.game_over False)
        for user in users:
            games = get_user_games(user)
            if games:
                subject = "This is a reminder!""
                body = "Hi {},"
                body += "You have open games of Tic-Tac-Toe!".format(user.name)
                body += 'The following games are still active:'
                for game in games:
                    body += str(game)
                body += "Good luck!"
                # This will send test emails, the arguments to send_mail are:
                # from, to, subject, body
                mail.send_mail('noreply@{}.appspotmail.com'.format(app_id),
                               user.email,
                               subject,
                               body)

app = webapp2.WSGIApplication([
    ('/crons/send_reminder', SendReminderEmail)
], debug=False)
