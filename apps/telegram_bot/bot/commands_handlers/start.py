from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from django.utils.translation import gettext_lazy as _

from apps.user.models import TelegramUser


class StartHandler:
    def __init__(self, updater):
        self.updater = updater

    def handle(self):
        tg_user, created = TelegramUser.objects.get_or_create(
            telegram_id=self.updater.body['message']['from']['id'],
            username=self.updater.body['message']['from'].get('username', ''),
            first_name=self.updater.body['message']['from']['first_name'],
            last_name=self.updater.body['message']['from'].get('last_name', '')
        )

        if created or not tg_user.lang:
            self.updater.bot.send_message(
                text='Choose language',
                chat_id=self.updater.body['message']['from']['id'],
                reply_markup=self.start_keyboard()
            )
        else:
            self.updater.bot.send_message(
                chat_id=self.updater.body['message']['from']['id'],
                text=str(_('tg_bot_greeting'))
            )

    @staticmethod
    def start_keyboard():
        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton(text='English', callback_data='set_lang:en'),
                InlineKeyboardButton(text='Українська', callback_data='set_lang:uk')
            ]
        ])
