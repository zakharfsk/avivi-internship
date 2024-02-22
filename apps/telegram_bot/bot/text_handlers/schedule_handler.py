import pytz
from datetime import datetime, timedelta
from typing import TYPE_CHECKING

from django.utils.translation import gettext_lazy as _

from telegram_bot_calendar import DetailedTelegramCalendar

from apps.telegram_bot.bot.states import State
from apps.telegram_bot.tasks import task_send_message

if TYPE_CHECKING:
    from apps.telegram_bot.bot.handler import UpdaterHandler

LSTEP_translate = {'y': _('year'), 'm': _('month'), 'd': _('day')}


class ScheduleHandler:
    def __init__(self, updater):
        self.updater: 'UpdaterHandler' = updater
        self.tg_user = self.updater.get_tg_user()

    def handle(self):
        self.tg_user.state = State.SET_SCHEDULE_DATE
        calendar_keyboard, step = DetailedTelegramCalendar().build()

        self.updater.bot.send_message(
            self.updater.body['chat']['id'],
            str(_("tg_bot_schedule_date")).format(step=LSTEP_translate[step]),
            reply_markup=calendar_keyboard
        )

        self.tg_user.save()

    def handle_callback(self):
        result, key, step = DetailedTelegramCalendar().process(self.updater.get_callback())

        if not result and key:
            self.updater.bot.edit_message_text(
                str(_("tg_bot_schedule_date")).format(step=LSTEP_translate[step]),
                self.updater.body['message']['chat']['id'],
                self.updater.body['message']['message_id'],
                reply_markup=key
            )
        elif result:
            self.tg_user.state = State.SET_SCHEDULE_TIME
            self.tg_user.state_data['date'] = str(result)
            self.tg_user.save()

            self.updater.bot.edit_message_text(
                str(_("tg_bot_schedule_time")).format(date=result),
                self.updater.body['message']['chat']['id'],
                self.updater.body['message']['message_id'],
            )

    def handle_time(self):
        self.tg_user.state = State.SET_SCHEDULE_TEXT

        try:
            self.tg_user.state_data['time'] = str(datetime.strptime(self.updater.body['text'], '%H:%M').time())
        except ValueError:
            self.updater.bot.send_message(
                self.updater.body['chat']['id'],
                str(_("tg_bot_invalid_time_format"))
            )
            return

        self.tg_user.save()

        self.updater.bot.send_message(
            self.updater.body['chat']['id'],
            str(_("tg_bot_schedule_text"))
        )

    def handle_task_text(self):
        self.tg_user.state_data['text'] = self.updater.body['text']
        self.tg_user.save()

        self.updater.bot.send_message(
            self.updater.body['chat']['id'],
            str(_("tg_bot_schedule_created")).format(
                date=self.tg_user.state_data['date'],
                time=self.tg_user.state_data['time'],
                text=self.tg_user.state_data['text']
            )
        )

        task_send_message.apply_async(
            args=[self.updater.bot.token, self.updater.body['chat']['id'], self.tg_user.state_data['text']],
            eta=(datetime.strptime(
                self.tg_user.state_data['date'] + ' ' + self.tg_user.state_data['time'],
                '%Y-%m-%d %H:%M:%S',
            ) + timedelta(minutes=2)).replace(tzinfo=pytz.timezone('Europe/Kiev'))
        )

        self.tg_user.state = State.NONE_STATE
        self.tg_user.state_data = {}
        self.tg_user.save()
