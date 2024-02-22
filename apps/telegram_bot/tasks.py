from telegram import Bot

from config.celery import app


@app.task
def task_send_message(token, chat_id, text):
    bot = Bot(token)
    bot.send_message(chat_id, text)
    return True
