import os
import logging

from telegram.ext import Updater

from commands import HANDLERS
from handlers.msg_handler import MESSAGE_HANDLER

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


token = os.environ.get('token')
updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher

# register all commands
for handler in HANDLERS:
    dispatcher.add_handler(handler)

dispatcher.add_handler(MESSAGE_HANDLER)

updater.start_polling()
