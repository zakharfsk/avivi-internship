from typing import TYPE_CHECKING

from apps.telegram_bot.tasks import task_send_user_tickets

if TYPE_CHECKING:
    from apps.telegram_bot.bot.handler import UpdaterHandler


class DownloadUserTickets:
    def __init__(self, updater):
        self.updater: 'UpdaterHandler' = updater
        self.tg_user = self.updater.get_tg_user()

    def handle(self):
        task_send_user_tickets.delay(
            token=self.updater.bot.token,
            chat_id=self.updater.body['from']['id'],
            user_id=self.tg_user.telegram_id
        )
