from django.utils import translation
from telegram import Bot
from django.utils.translation import gettext_lazy as _

from apps.telegram_bot.bot.callbacks import TypeCallBacks
from apps.telegram_bot.bot.callbacks_handlers.list_categories_callback import ListCategoriesCallBack
from apps.telegram_bot.bot.callbacks_handlers.setlang_callback import SetLangCallBack
from apps.telegram_bot.bot.callbacks_handlers.show_products import ProductsHandler
from apps.telegram_bot.bot.commands import BotCommand
from apps.telegram_bot.bot.commands_handlers.start import StartHandler
from apps.telegram_bot.bot.states import State
from apps.telegram_bot.bot.states_handler.enter_two_code_state import GetTwoAuthCodeHandler
from apps.telegram_bot.bot.text_commands import KeyboardTextCommand
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
        self.activate_lang()

        if BotCommand.START == self.get_command():
            StartHandler(self).handle()
            return

        if self.get_tg_user().state == State.ENTER_TWO_AUTH_CODE:
            GetTwoAuthCodeHandler(self).handle()
            return

        if self.get_callback_type() == TypeCallBacks.SET_LANG:
            SetLangCallBack(self).handle()

        if self.get_callback_type() == TypeCallBacks.SHOW_PRODUCTS or self.get_callback_type() == TypeCallBacks.SHOW_PRODUCT_BY_CAT_ID:
            ProductsHandler(self).handle()

        if self.get_callback_type() == TypeCallBacks.LIST_PRODUCT_CHANGE_PAGE:
            ProductsHandler(self).change_page()

        if self.get_callback_type() == TypeCallBacks.LIST_CATEGORIES_CHANGE_PAGE:
            ListCategoriesCallBack(self).handle()

        if self.body.get('text') == str(_(KeyboardTextCommand.CATALOG)):
            CatalogHandler(self).handle()

    def activate_lang(self):
        tg_user = TelegramUser.objects.filter(
            telegram_id=self.body['from']['id']
        )
        translation.activate(tg_user.first().lang if tg_user.exists() else 'en')

    def get_tg_user(self):
        return TelegramUser.objects.get(
            telegram_id=self.body['from']['id']
        )

    @staticmethod
    def is_command(message: dict):
        return True if message.get('message', {}).get('entities') else False

    @staticmethod
    def is_text_message(message: dict):
        return True if 'message' in message else False

    @staticmethod
    def is_callback(message: dict):
        return True if 'callback_query' in message else False

    @staticmethod
    def is_keyboard_command(message: dict):
        return True if not message.get('message', {}).get('text').startswith('/') else False

    def get_command(self):
        return self.body.get('text')

    def get_callback_type(self):
        return self.body.get('data', '').split(':')[0]

    def get_call_back_data(self):
        return self.body.get('data', '').split(':')[1]
