from typing import TYPE_CHECKING

from apps.telegram_bot.bot.text_handlers.catalog_handler import CatalogHandler

if TYPE_CHECKING:
    from apps.telegram_bot.bot.handler import UpdaterHandler


class ListCategoriesCallBack:
    def __init__(self, updater):
        self.updater: 'UpdaterHandler' = updater

    def handle(self):
        page = self.updater.get_call_back_data()
        CatalogHandler(self.updater).change_page(page)
