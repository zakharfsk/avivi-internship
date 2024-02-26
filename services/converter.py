import codecs
import json

import requests
from django.conf import settings
from django.template.loader import render_to_string

from apps.telegram_support.models import Ticket


def make_pdf_file(user_id: int):
    template = _render_template(user_id)
    response = _make_request(template)
    return response.content


def _render_template(user_id: int) -> str:
    return render_to_string(
        'support/pdf_template.html',
        {
            'tickets': Ticket.objects.filter(user__telegram_id=user_id).all()
        }
    )


def _make_request(html_template: str):
    return requests.post(
        settings.CONVERTER_PDF_SERVICE_FULL_URL,
        data=json.dumps({
            'contents': codecs.encode(html_template.encode(), 'base64').decode()
        }),
        headers={
            'Content-Type': 'application/json',
        }
    )
