from django.core.paginator import Paginator
from django.utils.translation import gettext_lazy as _
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from apps.product.models import Category


class CatalogHandler:
    def __init__(self, updater):
        self.updater = updater

    def handle(self):
        self.updater.bot.send_message(
            chat_id=self.updater.body['from']['id'],
            text=str(_('tg_bot_category_list')),
            reply_markup=self.categories_keyboard()
        )

    @staticmethod
    def get_pagination():
        return Paginator(Category.objects.all(), 3)

    def categories_keyboard(self, page=1):
        paginator = self.get_pagination().get_page(page)
        keyboard = InlineKeyboardMarkup(inline_keyboard=[])

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
                    callback_data=f'list_categories_next_page:{paginator.next_page_number()}'
                )
            ])

        if paginator.has_previous():
            keyboard.inline_keyboard.append([
                InlineKeyboardButton(
                    text='Previous',
                    callback_data=f'list_categories_prev_page:{paginator.previous_page_number()}'
                )
            ])

        return keyboard
