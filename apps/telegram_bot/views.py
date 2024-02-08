from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from apps.telegram_bot.forms import TelegramBotForm
from apps.telegram_bot.models import TelegramBot
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
    print(request.body.decode('utf-8'))
    return JsonResponse({'status': 'ok'})


def telegram_bot_set_webhook(request: WSGIRequest, pk: int):
    bot = TelegramBot.objects.get(pk=pk)
    absolute_uri = request.build_absolute_uri(reverse_lazy('telegram_bot:telegram_bots_webhook')).replace('http://',
                                                                                                          'https://')
    if bot.webhook_enabled:
        tg_api_response = bot.delete_webhook()
        bot.webhook_enabled = False
    else:
        tg_api_response = bot.set_webhook(absolute_uri)
        bot.webhook_enabled = True

    if tg_api_response['ok']:
        bot.save()

    return redirect(request.META['HTTP_REFERER'])
