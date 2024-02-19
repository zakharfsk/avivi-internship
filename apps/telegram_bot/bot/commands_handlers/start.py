from typing import TYPE_CHECKING

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from django.utils.translation import gettext_lazy as _

from apps.user.models import TelegramUser

if TYPE_CHECKING:
    from apps.telegram_bot.bot.handler import UpdaterHandler


class StartHandler:
    def __init__(self, updater):
        self.updater: 'UpdaterHandler' = updater

    def handle(self):
        tg_user, created = TelegramUser.objects.get_or_create(
            telegram_id=self.updater.body['from']['id'],
            username=self.updater.body['from'].get('username', ''),
            first_name=self.updater.body['from']['first_name'],
            last_name=self.updater.body['from'].get('last_name', '')
        )

        if created or not tg_user.lang:
            self.updater.bot.send_message(
                text='Choose language',
                chat_id=self.updater.body['from']['id'],
                reply_markup=self.start_inline_keyboard()
            )
        else:
            self.updater.bot.send_message(
                chat_id=self.updater.body['from']['id'],
                text=str(_('tg_bot_greeting')),
                reply_markup=self.start_reply_keyboard()
            )

    @staticmethod
    def start_inline_keyboard():
        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton(text='English', callback_data='set_lang:en'),
                InlineKeyboardButton(text='Українська', callback_data='set_lang:uk')
            ]
        ])

    @staticmethod
    def start_reply_keyboard():
        return ReplyKeyboardMarkup([
            [
                KeyboardButton(str(_('tg_bot_keyboard_button_catalog')))
            ],
        ], resize_keyboard=True)
