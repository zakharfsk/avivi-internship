from typing import TYPE_CHECKING

from django.utils import translation
from django.utils.translation import gettext_lazy as _

from apps.telegram_bot.bot.commands_handlers.start import StartHandler
from apps.user.models import TelegramUser

if TYPE_CHECKING:
    from apps.telegram_bot.bot.handler import UpdaterHandler


class SetLangCallBack:
    def __init__(self, updater):
        self.updater: 'UpdaterHandler' = updater

    def handle(self):
        lang = self.updater.body['data'].split(':')[1]
        TelegramUser.objects.filter(telegram_id=self.updater.body['from']['id']).update(
            lang=lang
        )

        translation.activate(lang)
        self.updater.bot.edit_message_text(
            chat_id=self.updater.body['from']['id'],
            message_id=self.updater.body['message']['message_id'],
            text=str(_('tg_bot_greeting')),
            reply_markup=StartHandler.start_reply_keyboard()
        )
