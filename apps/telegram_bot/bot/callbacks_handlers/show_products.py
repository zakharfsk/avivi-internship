from typing import TYPE_CHECKING

from django.conf import settings
from django.core.paginator import Paginator
from django.utils.translation import gettext_lazy as _
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode

from apps.product.models import Product
from apps.telegram_bot.bot.callbacks import TypeCallBacks

if TYPE_CHECKING:
    from apps.telegram_bot.bot.handler import UpdaterHandler


class ProductsHandler:
    def __init__(self, updater):
        self.updater: 'UpdaterHandler' = updater

    def handle(self, page: int = 1):
        callback_type = self.updater.get_callback_type()

        if callback_type == TypeCallBacks.SHOW_PRODUCT_BY_CAT_ID:
            cat_id = int(self.updater.get_call_back_data())
            keyboard, page = self.product_keyboard(page, cat_id)

        if callback_type == TypeCallBacks.SHOW_PRODUCTS:
            keyboard, page = self.product_keyboard(page)

        product: Product = page.object_list[0]

        self.updater.bot.send_photo(
            chat_id=self.updater.body['from']['id'],
            photo=settings.DEFAULT_DOMAIN + product.photo.url,
            caption=f'{product.name}\n\n'
                    f'<b>{_('tg_bot_product_price')}:</b> {product.price} UAH\n'
                    f'<b>{_('tg_bot_product_colour')}:</b> {product.colour}\n'
                    f'<b>{_('tg_bot_product_brand')}:</b> {product.brand}\n'
                    f'<b>{_('tg_bot_product_size')}:</b> {product.size}',
            reply_markup=keyboard,
            parse_mode=ParseMode.HTML
        )

    def change_page(self):
        callback_data = self.updater.body['data'].split(':')
        if len(callback_data) == 2:
            page = int(callback_data[1])
            cat_id = None
        else:
            page = int(callback_data[1])
            cat_id = int(callback_data[2])

        keyboard, page = self.product_keyboard(page, cat_id)
        self.updater.bot.delete_message(
            chat_id=self.updater.body['message']['chat']['id'],
            message_id=self.updater.body['message']['message_id']
        )
        self.updater.bot.send_photo(
            chat_id=self.updater.body['from']['id'],
            photo=settings.DEFAULT_DOMAIN + page.object_list[0].photo.url,
            caption=f'{page.object_list[0].name}\n\n'
                    f'<b>{_('tg_bot_product_price')}:</b> {page.object_list[0].price} UAH\n'
                    f'<b>{_('tg_bot_product_colour')}:</b> {page.object_list[0].colour}\n'
                    f'<b>{_('tg_bot_product_brand')}:</b> {page.object_list[0].brand}\n'
                    f'<b>{_('tg_bot_product_size')}:</b> {page.object_list[0].size}',
            reply_markup=keyboard,
            parse_mode=ParseMode.HTML
        )

    @staticmethod
    def get_product_pagination(per_page: int = 1, cat_id: int | None = None):
        if cat_id:
            return Paginator(Product.objects.filter(category_id=cat_id), per_page)

        return Paginator(Product.objects.all(), per_page)

    def product_keyboard(self, page: int, cat_id: int | None = None):
        paginator = self.get_product_pagination(cat_id=cat_id).get_page(page)
        keyboard = InlineKeyboardMarkup(inline_keyboard=[])

        if paginator.has_next():
            keyboard.inline_keyboard.append([
                InlineKeyboardButton(
                    text='Next',
                    callback_data=f'list_product_change_page:{paginator.next_page_number()}' + (
                        f':{cat_id}' if cat_id else '')
                )
            ])

        if paginator.has_previous():
            keyboard.inline_keyboard.append([
                InlineKeyboardButton(
                    text='Previous',
                    callback_data=f'list_product_change_page:{paginator.previous_page_number()}' + (
                        f':{cat_id}' if cat_id else '')
                )
            ])

        return keyboard, paginator
