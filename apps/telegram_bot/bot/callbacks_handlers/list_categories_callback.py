class ListCategoriesCallBack:
    def __init__(self, updater):
        self.updater = updater

    def handle(self):
        self.updater.bot.send_message(
            chat_id=self.updater.body['from']['id'],
            text='categories',
            # reply_markup=self.categories_keyboard()
        )

