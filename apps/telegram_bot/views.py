import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import translation
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup

from apps.telegram_bot.bot.callbacks import TypeCallBacks
from apps.telegram_bot.bot.commands import BotCommand
from apps.telegram_bot.forms import TelegramBotForm
from apps.telegram_bot.models import TelegramBot
from apps.user.models import TelegramUser
from common.mixins import SuperUserRequiredMixin, TitleMixin


class TelegramBotListView(TitleMixin, LoginRequiredMixin, SuperUserRequiredMixin, ListView):
    model = TelegramBot
    paginate_by = 3
    title = 'Telegram bots'
    template_name = 'telegram_bots/telegram_bots_list.html'


class TelegramBotDetailView(TitleMixin, LoginRequiredMixin, SuperUserRequiredMixin, DetailView):
    model = TelegramBot
    title = 'Telegram bot detail'
    template_name = 'telegram_bots/telegram_bots_detail.html'


class TelegramBotCreateView(TitleMixin, LoginRequiredMixin, SuperUserRequiredMixin, CreateView):
    model = TelegramBot
    form_class = TelegramBotForm
    title = 'Create Telegram bot'
    template_name = 'telegram_bots/telegram_bots_create.html'
    success_url = reverse_lazy('telegram_bot:telegram_bots')


class TelegramBotUpdateView(TitleMixin, LoginRequiredMixin, SuperUserRequiredMixin, UpdateView):
    model = TelegramBot
    form_class = TelegramBotForm
    title = 'Update Telegram bot'
    template_name = 'telegram_bots/telegram_bots_update.html'
    success_url = reverse_lazy('telegram_bot:telegram_bots')


class TelegramBotDeleteView(TitleMixin, LoginRequiredMixin, SuperUserRequiredMixin, DeleteView):
    model = TelegramBot
    title = 'Delete Telegram bot'
    template_name = 'telegram_bots/telegram_bots_delete.html'
    success_url = reverse_lazy('telegram_bot:telegram_bots')


@csrf_exempt
def telegram_bot_webhook_view(request: WSGIRequest):
    decode_body = json.loads(request.body.decode('utf-8'))
    bot = Bot(token=TelegramBot.objects.first().token)

    load_body = decode_body if decode_body.get("message") else decode_body.get("callback_query")
    is_callback_query = bool(decode_body.get("callback_query"))
    is_command = load_body['message']['text'].startswith('/')
    type_callback = load_body['data'].split(':')[0] if is_callback_query else None

    tg_user = TelegramUser.objects.filter(telegram_id=load_body['message']['from']['id'])

    if tg_user.exists():
        translation.activate(tg_user.first().lang)

    if is_command:
        if load_body['message']['text'] == BotCommand.START:
            if not tg_user.exists():
                TelegramUser.objects.create(
                    telegram_id=load_body['message']['from']['id'],
                    username=load_body['message']['from'].get('username', ''),
                    first_name=load_body['message']['from']['first_name'],
                    last_name=load_body['message']['from'].get('last_name', '')
                )
                bot.send_message(
                    text='Choose language',
                    chat_id=load_body['message']['from']['id'],
                    reply_markup=InlineKeyboardMarkup(
                        inline_keyboard=[
                            [
                                InlineKeyboardButton(text='English', callback_data='set_lang:en'),
                                InlineKeyboardButton(text='Українська', callback_data='set_lang:uk')
                            ],
                        ]
                    )
                )
            else:
                bot.send_message(
                    chat_id=load_body['message']['from']['id'],
                    text=str(_('tg_bot_greeting'))
                )
        else:
            bot.send_message(
                chat_id=load_body['message']['from']['id'],
                text=str(_('tg_bot_unknown_command'))
            )

    if is_callback_query:
        if type_callback == TypeCallBacks.SET_LANG:
            TelegramUser.objects.filter(telegram_id=load_body['from']['id']).update(
                lang=load_body['data'].split(':')[1]
            )
            translation.activate(load_body['data'].split(':')[1])

            bot.edit_message_text(
                chat_id=load_body['from']['id'],
                message_id=load_body['message']['message_id'],
                text=str(_('tg_bot_greeting'))
            )

        if type_callback == TypeCallBacks.CHANGE_LANG:
            pass

    translation.deactivate()
    return JsonResponse({'status': 'ok'})


@login_required
def telegram_bot_set_webhook(request: WSGIRequest, pk: int):
    bot = TelegramBot.objects.get(pk=pk)
    tg_bot_obj = Bot(token=bot.token)
    absolute_uri = request.build_absolute_uri(
        reverse_lazy('telegram_bot:telegram_bots_webhook')
    ).replace('http://', 'https://')

    if bot.webhook_enabled:
        webhook = tg_bot_obj.delete_webhook()
        bot.webhook_enabled = False
    else:
        webhook = tg_bot_obj.set_webhook(absolute_uri)
        bot.webhook_enabled = True

    if webhook:
        bot.save()

    return redirect(request.META['HTTP_REFERER'])
