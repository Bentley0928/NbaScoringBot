#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import requests

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

api_base_url = "http://data.nba.net/10s"
# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)

def get_scoreboard():
    index = requests.get(api_base_url + "/prod/v1/today.json").json()
    scoreboard_url = index["links"]["todayScoreboard"]
    return scoreboard_url

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    chat_id = update.message.chat.id
    print(chat_id)
    """Send a message when the command /start is issued."""
    update.message.reply_text("請輸入要查詢之日期(格式如20210331)，如要查詢目前請輸入today，如在群組內，請回覆此則訊息")


"""
def echo(update, context):
   #Echo the user message.
    update.message.reply_text(update.message.text)
"""


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def getscore(update, context):
    command = update.message.text
    """
    print(command)
    chat_id = update.message.chat.id
    print(chat_id)
    """
    if command == "today":
        print(command)
        scoreboard = requests.get(api_base_url + get_scoreboard()).json()
        if not 'games' in scoreboard or len(scoreboard['games']) == 0:
            update.message.reply_text("今天沒有球賽呦<3")
        else:
            output = "主場 / 客場 / 節數"
            for game in scoreboard["games"]:
                output += game["vTeam"]["triCode"] + ":" + game["vTeam"]["score"]
                output += " / "
                output += game["hTeam"]["triCode"] + ":" + game["hTeam"]["score"]
                output += " / "
                output += str(game["period"]["current"]) + " " + str(game["clock"]) + "\n"
            update.message.reply_text(output)
    else:
        print(command)
        scoreboard = requests.get("http://data.nba.net/prod/v1/" + command + "/scoreboard.json").json()
        print(scoreboard['numGames'])
        if not 'gmaes' in scoreboard or len(scoreboard['games']) == 0:
            update.message.reply_text("今天沒有球賽呦<3")
        else:
            output = "主場 / 客場 / 節數"
            for game in scoreboard["games"]:
                output += game["vTeam"]["triCode"] + ":" + game["vTeam"]["score"]
                output += " / "
                output += game["hTeam"]["triCode"] + ":" + game["hTeam"]["score"]
                output += " / "
                output += str(game["period"]["current"]) + " " + str(game["clock"]) + "\n"
            update.message.reply_text(output)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("1707087781:AAHKyP3CIkapFZQR2Kfnxz1_t3AObvzsLjM", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, getscore))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()
    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == "__main__":
    main()