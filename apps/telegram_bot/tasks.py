from io import BytesIO

from telegram import Bot

from config.celery import app
from services.converter import make_pdf_file


@app.task
def task_send_message(token, chat_id, text):
    bot = Bot(token)
    bot.send_message(chat_id, text)
    return True


@app.task
def task_send_user_tickets(token, chat_id, user_id):
    bot = Bot(token)

    pdf_file_content = make_pdf_file(user_id)

    if not pdf_file_content:
        return False

    pdf_file = BytesIO(pdf_file_content)
    pdf_file.name = 'tickets.pdf'
    bot.send_document(
        chat_id=chat_id,
        document=pdf_file
    )

    # bot.send_document(
    #     chat_id=chat_id,
    #     document=buffer.getvalue()
    # )
    return True
