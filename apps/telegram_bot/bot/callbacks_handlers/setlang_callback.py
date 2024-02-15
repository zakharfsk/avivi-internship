from django.utils import translation
from django.utils.translation import gettext_lazy as _
from telegram import ReplyKeyboardRemove

from apps.user.models import TelegramUser


class SetLangCallBack:
    def __init__(self, updater):
        self.updater = updater

    def handle(self):
        lang = self.updater.body['data'].split(':')[1]
        TelegramUser.objects.filter(telegram_id=self.updater.body['from']['id']).update(
            lang=lang
        )

        translation.activate(lang)
        self.updater.bot.edit_message_text(
            chat_id=self.updater.body['from']['id'],
            message_id=self.updater.body['message_id'],
            text=str(_('tg_bot_greeting'))
        )
