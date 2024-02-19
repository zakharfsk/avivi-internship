from typing import TYPE_CHECKING
from django.utils.translation import gettext_lazy as _

from apps.telegram_bot.bot.two_auth import verify_totp

if TYPE_CHECKING:
    from apps.telegram_bot.bot.handler import UpdaterHandler


class GetTwoAuthCodeHandler:
    def __init__(self, updater):
        self.updater: 'UpdaterHandler' = updater

    def handle(self):
        if not verify_totp(self.updater.body['text']):
            self.updater.bot.send_message(
                chat_id=self.updater.body['from']['id'],
                text=str(_('tg_bot_wrong_code'))
            )
            return

        tg_user = self.updater.get_tg_user()
        tg_user.two_auth_enabled = True
        tg_user.state = ''
        tg_user.save()

        self.updater.bot.send_message(
            chat_id=self.updater.body['from']['id'],
            text=str(_('tg_bot_two_auth_enabled'))
        )
