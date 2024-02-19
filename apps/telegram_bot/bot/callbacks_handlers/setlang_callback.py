from typing import TYPE_CHECKING

from django.conf import settings
from django.utils import translation
from django.utils.translation import gettext_lazy as _
from telegram import ParseMode

from apps.telegram_bot.bot.commands_handlers.start import StartHandler
from apps.telegram_bot.bot.states import State
from apps.telegram_bot.bot.utils import get_qr_image

if TYPE_CHECKING:
    from apps.telegram_bot.bot.handler import UpdaterHandler


class SetLangCallBack:
    def __init__(self, updater):
        self.updater: 'UpdaterHandler' = updater

    def handle(self):
        lang = self.updater.body['data'].split(':')[1]
        tg_user = self.updater.get_tg_user()
        tg_user.lang = lang

        translation.activate(lang)

        self.updater.bot.delete_message(
            chat_id=self.updater.body['from']['id'],
            message_id=self.updater.body['message']['message_id']
        )
        self.updater.bot.send_message(
            chat_id=self.updater.body['from']['id'],
            text=str(_('tg_bot_greeting')),
            reply_markup=StartHandler.start_reply_keyboard()
        )

        if not tg_user.two_auth_enabled:
            self.updater.bot.send_photo(
                chat_id=self.updater.body['from']['id'],
                caption=str(_('tg_bot_two_auth_not_enabled')).format(code=settings.OTP_SECRET_KEY),
                photo=get_qr_image(),
                parse_mode=ParseMode.HTML
            )
            tg_user.state = State.ENTER_TWO_AUTH_CODE

        tg_user.save()
