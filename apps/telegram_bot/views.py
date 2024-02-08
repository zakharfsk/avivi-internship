from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
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