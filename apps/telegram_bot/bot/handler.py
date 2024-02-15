from django.utils import translation
from telegram import Bot
from django.utils.translation import gettext_lazy as _

from apps.telegram_bot.bot.callbacks import TypeCallBacks
from apps.telegram_bot.bot.callbacks_handlers.setlang_callback import SetLangCallBack
from apps.telegram_bot.bot.commands import BotCommand
from apps.telegram_bot.bot.commands_handlers.start import StartHandler
from apps.telegram_bot.bot.text_handlers.catalog_handler import CatalogHandler
from apps.user.models import TelegramUser


class UpdaterHandler:
    def __init__(self, body: dict, bot: Bot):
        if self.is_command(body) or self.is_text_message(body):
            self.body = body['message']
        else:
            self.body = body['callback_query']
        self.bot = bot

    def handle(self):
        print(self.body)
        self.activate_lang()

        if BotCommand.START == self.get_command():
            StartHandler(self).handle()

        if self.get_callback_type() == TypeCallBacks.SET_LANG:
            SetLangCallBack(self).handle()

        if self.get_callback_type() == TypeCallBacks.SHOW_PRODUCT_BY_CAT_ID:
            pass

        if self.body.get('text') == str(_('tg_bot_keyboard_button_catalog')):
            CatalogHandler(self).handle()

    def activate_lang(self):
        tg_user = TelegramUser.objects.filter(
            telegram_id=self.body['from']['id']
        )
        translation.activate(tg_user.first().lang if tg_user.first().lang else 'en')

    def is_command(self, message: dict):
        return True if message.get('message', {}).get('entities') else False

    def is_text_message(self, message: dict):
        return True if 'message' in message else False

    def is_callback(self, message):
        return True if 'callback_query' in message else False

    def is_keyboard_command(self, message: dict):
        return True if not message.get('message', {}).get('text').startswith('/') else False

    def get_command(self):
        return self.body.get('text')

    def get_callback_type(self):
        return self.body.get('data', '').split(':')[0]
