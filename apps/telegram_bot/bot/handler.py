from django.utils import translation
from telegram import Bot
from django.utils.translation import gettext_lazy as _

from apps.telegram_bot.bot.callbacks import TypeCallBacks
from apps.telegram_bot.bot.callbacks_handlers.setlang_callback import SetLangCallBack
from apps.telegram_bot.bot.commands import BotCommand
from apps.telegram_bot.bot.commands_handlers.start import StartHandler
from apps.user.models import TelegramUser


class UpdateHandler:
    def __init__(self, body: dict, bot: Bot):
        self.body = body
        self.bot = bot

    def handle(self):
        self.activate_lang()

        if self.is_command():
            if BotCommand.START == self.get_command():
                StartHandler(self).handle()
            else:
                self.bot.send_message(
                    chat_id=self.body['message']['from']['id'],
                    text=str(_('tg_bot_unknown_command'))
                )

        if self.is_callback():
            if self.get_callback_type() == TypeCallBacks.SET_LANG:
                SetLangCallBack(self).handle()

    def activate_lang(self):
        tg_user = TelegramUser.objects.filter(
            telegram_id=self.body['message']['from']['id'] if self.is_command() else self.body['callback_query']['from']['id']
        )
        translation.activate(tg_user.first().lang if tg_user.first().lang else 'en')

    def is_command(self):
        return True if self.body.get('message') else False

    def is_callback(self):
        return True if self.body.get('callback_query') else False

    def get_command(self):
        return self.body['message']['text']

    def get_callback_type(self):
        return self.body['callback_query']['data'].split(':')[0]
