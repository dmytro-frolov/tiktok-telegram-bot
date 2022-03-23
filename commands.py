import os

from telegram import Update
from telegram.ext import CallbackContext, CommandHandler

from handlers.tiktok_handler import TTHandler


def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


def help(update: Update, context: CallbackContext):
    text = \
        """
/start: to start bot
/help: this help
/cookie HEADER: To set global cookies. Only admins can do
/remove_origin True/False: To remove origin message. Admin access required
        """
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


def cookie(update: Update, context: CallbackContext):
    if update.effective_user in [admin.user for admin in update.effective_chat.get_administrators()] is False:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Only admins can set cookies")
        return

    if text := update.message.text:
        cookie = text.split('/cookie')[-1].strip()
        TTHandler.set_cookie(cookie)
        context.bot.send_message(chat_id=update.effective_chat.id, text="Cookies are set")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="ERROR")


def remove_origin(update: Update, context: CallbackContext):
    text = update.message.text.split('/remove_origin', 1)
    if len(text) == 2:
        os.environ['REMOVE_ORIGIN'] = 'True' if text[1].strip() == "True" else 'False'
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Remove origin is {os.environ['REMOVE_ORIGIN']}")


HANDLERS = [
    CommandHandler('start', start),
    CommandHandler('help', help),
    CommandHandler('cookie', cookie),
    CommandHandler('remove_origin', remove_origin),
]
