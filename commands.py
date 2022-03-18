from telegram import Update
from telegram.ext import CallbackContext, CommandHandler

from handlers.tiktok_handler import TTHandler


def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


def help(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="There's no help for you, bitch!")


def cookie(update: Update, context: CallbackContext):
    if text := update.message.text:
        cookie = text.split('/cookie')[-1].strip()
        TTHandler.set_cookie(cookie)
        context.bot.send_message(chat_id=update.effective_chat.id, text="Cookies are set")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="ERROR")


HANDLERS = [
    CommandHandler('start', start),
    CommandHandler('help', help),
    CommandHandler('cookie', cookie),

]
