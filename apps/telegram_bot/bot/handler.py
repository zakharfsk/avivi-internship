from django.utils import translation
from telegram import Bot, Update
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
from apps.telegram_bot.bot.text_handlers.download_user_tickets import DownloadUserTickets
from apps.telegram_bot.bot.text_handlers.schedule_handler import ScheduleHandler
from apps.telegram_bot.bot.text_handlers.support_handler import SupportHandler
from apps.user.models import TelegramUser


class UpdaterHandler:
    def __init__(self, body: dict, bot: Bot):
        if self.is_command(body) or self.is_text_message(body):
            self.body = body['message']
        else:
            self.body = body['callback_query']
        self.bot = bot
        self.update = Update.de_json(body, bot)
        # self.update.
        print(self.update.callback_query)
        print(self.update.message)

    def handle(self):
        self.activate_lang()

        if BotCommand.START == self.get_command():
            StartHandler(self).handle()
            return

        tg_user = self.get_tg_user()

        if tg_user.state == State.ENTER_TWO_AUTH_CODE:
            GetTwoAuthCodeHandler(self).handle()
            return

        if (
            tg_user.state == State.WRITE_SUPPORT_TITLE or
            tg_user.state == State.WRITE_SUPPORT_DESCRIPTION or
            tg_user.state == State.WRITE_SUPPORT_ENTER_TWO_AUTH_CODE
        ):
            SupportHandler(self).handle()
            return

        if self.get_callback_type() == TypeCallBacks.SET_LANG:
            SetLangCallBack(self).handle()
            return

        if (
            self.get_callback_type() == TypeCallBacks.SHOW_PRODUCTS or
            self.get_callback_type() == TypeCallBacks.SHOW_PRODUCT_BY_CAT_ID
        ):
            ProductsHandler(self).handle()
            return

        if self.get_callback_type() == TypeCallBacks.LIST_PRODUCT_CHANGE_PAGE:
            ProductsHandler(self).change_page()
            return

        if self.get_callback_type() == TypeCallBacks.LIST_CATEGORIES_CHANGE_PAGE:
            ListCategoriesCallBack(self).handle()
            return

        if TypeCallBacks.CALENDAR_CALLBACK in self.get_callback() and tg_user.state == State.SET_SCHEDULE_DATE:
            ScheduleHandler(self).handle_callback()
            return

        if tg_user.state == State.SET_SCHEDULE_TIME:
            ScheduleHandler(self).handle_time()
            return

        if tg_user.state == State.SET_SCHEDULE_TEXT:
            ScheduleHandler(self).handle_task_text()
            return

        if self.body.get('text') == str(_(KeyboardTextCommand.CATALOG)):
            CatalogHandler(self).handle()
            return

        if self.body.get('text') == str(_(KeyboardTextCommand.WRITE_TO_SUPPORT)):
            SupportHandler(self).handle()
            return

        if self.body.get('text') == str(_(KeyboardTextCommand.SET_SCHEDULE)):
            ScheduleHandler(self).handle()

        if self.body.get('text') == str(_(KeyboardTextCommand.DOWNLOAD_USER_TICKETS)):
            DownloadUserTickets(self).handle()

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
        return self.body.get('text', '')

    def get_callback(self):
        return self.body.get('data', '')

    def get_callback_type(self):
        return self.body.get('data', '').split(':')[0]

    def get_call_back_data(self):
        return self.body.get('data', '').split(':')[1]
