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
from apps.telegram_bot.bot.handler import UpdateHandler
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
    bot = Bot(token=TelegramBot.objects.first().token)
    decode_body = json.loads(request.body.decode('utf-8'))

    updater = UpdateHandler(
        decode_body,
        bot
    )
    updater.handle()

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
