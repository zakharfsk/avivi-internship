from typing import TYPE_CHECKING

from apps.telegram_bot.bot.states import State
from apps.telegram_support.models import Ticket

if TYPE_CHECKING:
    from apps.telegram_bot.bot.handler import UpdaterHandler


class SupportHandler:
    def __init__(self, updater):
        self.updater: 'UpdaterHandler' = updater

    def handle(self):
        tg_user = self.updater.get_tg_user()
        ticket, _ = Ticket.objects.get_or_create(user=tg_user)

        if tg_user.state == State.NONE_STATE:
            self.updater.bot.send_message(
                chat_id=tg_user.telegram_id,
                text='Write your title message'
            )
            tg_user.state = State.WRITE_SUPPORT_TITLE

        if tg_user.state == State.WRITE_SUPPORT_TITLE:
            self.updater.bot.send_message(
                chat_id=tg_user.telegram_id,
                text='Write your description message'
            )
            ticket.title = self.updater.body['text']
            tg_user.state = State.WRITE_SUPPORT_DESCRIPTION

        if tg_user.state == State.WRITE_SUPPORT_DESCRIPTION:
            ticket.description = self.updater.body['text']
            self.updater.bot.send_message(
                chat_id=tg_user.telegram_id,
                text='Your ticket was created'
            )
            tg_user.state = State.NONE_STATE
