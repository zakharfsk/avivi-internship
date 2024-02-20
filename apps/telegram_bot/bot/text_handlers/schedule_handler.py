import calendar
import datetime
from typing import TYPE_CHECKING

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP

if TYPE_CHECKING:
    from apps.telegram_bot.bot.handler import UpdaterHandler


class ScheduleHandler:
    def __init__(self, updater):
        self.updater: 'UpdaterHandler' = updater

    def handle(self):
        calendar, step = DetailedTelegramCalendar().build()
        self.updater.bot.send_message(
            self.updater.body['chat']['id'],
            f"Select {LSTEP[step]}",
            reply_markup=calendar
        )

    def handle_callback(self):
        result, key, step = DetailedTelegramCalendar().process(self.updater.get_callback())
        if not result and key:
            self.updater.bot.edit_message_text(
                f"Select {LSTEP[step]}",
                self.updater.body['message']['chat']['id'],
                self.updater.body['message']['message_id'],
                reply_markup=key
            )
        elif result:
            self.updater.bot.edit_message_text(
                f"You selected {result}",
                self.updater.body['message']['chat']['id'],
                self.updater.body['message']['message_id'],
            )
