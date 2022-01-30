from telegram import Update
from telegram.ext import CallbackContext, CommandHandler


def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


def help(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="There's no help for you, bitch!")


HANDLERS = [
    CommandHandler('start', start),
    CommandHandler('help', help),
]
