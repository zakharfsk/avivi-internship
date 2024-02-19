from typing import TYPE_CHECKING

from django.core.paginator import Paginator
from django.utils.translation import gettext_lazy as _
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from apps.product.models import Category

if TYPE_CHECKING:
    from apps.telegram_bot.bot.handler import UpdaterHandler


class CatalogHandler:
    def __init__(self, updater):
        self.updater: 'UpdaterHandler' = updater

    def handle(self, page=1):
        self.get_category_pagination().get_page(page)
        self.updater.bot.send_message(
            chat_id=self.updater.body['from']['id'],
            text=str(_('tg_bot_category_list')),
            reply_markup=self.categories_keyboard(page)
        )

    def change_page(self, page):
        self.updater.bot.edit_message_reply_markup(
            chat_id=self.updater.body['message']['chat']['id'],
            message_id=self.updater.body['message']['message_id'],
            reply_markup=self.categories_keyboard(page)
        )

    @staticmethod
    def get_category_pagination(per_page=3):
        return Paginator(Category.objects.all(), per_page)

    def categories_keyboard(self, page):
        paginator = self.get_category_pagination().get_page(page)
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=str(_('tg_bot_product_list')), callback_data='show_products')]
        ])

        keyboard.inline_keyboard.extend(
            [
                [InlineKeyboardButton(text=str(page), callback_data=f'show_product_by_cat_id:{page.id}')
                 for page in paginator]
            ]
        )

        if paginator.has_next():
            keyboard.inline_keyboard.append([
                InlineKeyboardButton(
                    text='Next',
                    callback_data=f'list_categories_change_page:{paginator.next_page_number()}'
                )
            ])

        if paginator.has_previous():
            keyboard.inline_keyboard.append([
                InlineKeyboardButton(
                    text='Previous',
                    callback_data=f'list_categories_change_page:{paginator.previous_page_number()}'
                )
            ])

        return keyboard
