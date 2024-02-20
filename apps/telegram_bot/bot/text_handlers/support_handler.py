from typing import TYPE_CHECKING

from apps.telegram_bot.bot.states import State
from django.utils.translation import gettext_lazy as _
from apps.telegram_bot.bot.two_auth import verify_totp
from apps.telegram_support.models import Ticket

if TYPE_CHECKING:
    from apps.telegram_bot.bot.handler import UpdaterHandler


class SupportHandler:
    def __init__(self, updater):
        self.updater: 'UpdaterHandler' = updater

    def handle(self):
        tg_user = self.updater.get_tg_user()

        if tg_user.state == State.NONE_STATE:
            self.updater.bot.send_message(
                chat_id=tg_user.telegram_id,
                text=str(_('tg_bot_support_title'))
            )
            tg_user.state = State.WRITE_SUPPORT_TITLE
            tg_user.state_data = {}
            tg_user.save()
            return

        if tg_user.state == State.WRITE_SUPPORT_TITLE:
            self.updater.bot.send_message(
                chat_id=tg_user.telegram_id,
                text=str(_('tg_bot_support_description'))
            )
            tg_user.state_data['title'] = self.updater.body['text']
            tg_user.state = State.WRITE_SUPPORT_DESCRIPTION
            tg_user.save()
            return

        if tg_user.state == State.WRITE_SUPPORT_DESCRIPTION:
            tg_user.state_data['description'] = self.updater.body['text']

            self.updater.bot.send_message(
                chat_id=tg_user.telegram_id,
                text=str(_('tg_bot_support_two_auth'))
            )

            tg_user.state = State.WRITE_SUPPORT_ENTER_TWO_AUTH_CODE
            tg_user.save()
            return

        if tg_user.state == State.WRITE_SUPPORT_ENTER_TWO_AUTH_CODE:
            if not verify_totp(self.updater.body['text']):
                self.updater.bot.send_message(
                    chat_id=self.updater.body['from']['id'],
                    text=str(_('tg_bot_wrong_code'))
                )
                return

            Ticket.objects.create(**tg_user.state_data, user=tg_user)
            self.updater.bot.send_message(
                chat_id=self.updater.body['from']['id'],
                text=str(_('tg_bot_ticket_created'))
            )
            tg_user.state = State.NONE_STATE
            tg_user.state_data = {}
            tg_user.save()
