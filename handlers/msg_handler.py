import os
import re

from telegram import Update, ParseMode, error
from telegram.ext import MessageHandler, Filters, CallbackContext

from handlers.tiktok_handler import TTHandler
from models import User, session, CacheLink


def msg_handler(update: Update, context: CallbackContext):
    if tt_link := re.findall(".*(https://.*tiktok.com/.*?)($|\s)", update.message.text):
        page_url = tt_link[0][0]

        with session() as s:
            #todo: get user id in model method
            user = s.query(User).filter_by(user_id=update.effective_user.id).first()
            if not user:
                user = User(user_id=update.effective_user.id,
                         name=update.effective_user.username)
                s.add(user)
                s.commit()

            cache_link_exist = s.query(CacheLink).filter_by(page_url=page_url).first()
            if cache_link_exist and not cache_link_exist.archived:
                notify(update, context, page_url, cache_link_exist.video_link)
                return

            tt = TTHandler(page_url)
            if tt.is_captcha():
                context.bot.send_message(chat_id=update.effective_chat.id, text='Page contains captcha')
                return

            video_link = tt.get_video_link()
            notify(update, context, page_url, video_link)

            cache_link = CacheLink(page_url=page_url, video_link=video_link, user_id=user.id)
            s.add(cache_link)
            s.commit()


def notify(update, context, page_url, video_link):
    if video_link:
        formatted_tt_link = f"<a href='{video_link}'>Video link</a>"
        text = update.message.text.replace(page_url, formatted_tt_link)
        if not update.effective_message.from_user.is_bot:
            text = f">{update.effective_message.from_user.username}: \n{text}"

        context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode=ParseMode.HTML,
                                 disable_notification=True, disable_web_page_preview=False)
        try:

            if os.environ.get('REMOVE_ORIGIN', False) == 'True':
                update.message.delete()
        except error.BadRequest as e:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="Can't remove origin message. Check permissions", parse_mode=ParseMode.HTML)
        return

    output_text = "Could not parse link"
    context.bot.send_message(chat_id=update.effective_chat.id, text=output_text)


MESSAGE_HANDLER = MessageHandler(Filters.text & (~Filters.command), msg_handler)
