import re

from telegram import Update, ParseMode
from telegram.ext import MessageHandler, Filters, CallbackContext

from handlers.tiktok_handler import TTHandler


def msg_handler(update: Update, context: CallbackContext):
    input_text = update.message.text
    if tt_link := re.findall(".*(https://.*tiktok.com/.*?)($|\s)", input_text):
        link = tt_link[0][0]

        tt = TTHandler(link)

        if tt.is_captcha():
            context.bot.send_message(chat_id=update.effective_chat.id, text='Page contains captcha')
            return

        if video_link := tt.get_video_link():
            formatted_tt_link = f"<a href='{video_link}'>Video link</a>"
            text = input_text.replace(link, formatted_tt_link)
            context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode=ParseMode.HTML)
            return

        output_text = "Could not parse link"
        context.bot.send_message(chat_id=update.effective_chat.id, text=output_text)


MESSAGE_HANDLER = MessageHandler(Filters.text & (~Filters.command), msg_handler)
