from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

from .forms import TelegramUserForm, UserLoginForm, UserRegistrationForm
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView

from common.mixins import GroupRequiredMixin, TitleMixin
from .models import TelegramUser, User


class UserLoginView(TitleMixin, LoginView):
    title = 'Авторизація'
    form_class = UserLoginForm
    success_url = reverse_lazy('user:profile')
    template_name = 'user/auth/login.html'


class UserRegistrationCreateView(TitleMixin, CreateView):
    title = 'Реєстрація'
    model = User
    form_class = UserRegistrationForm
    success_url = reverse_lazy('user:login')
    template_name = 'user/auth/register.html'


class UserProfileView(TitleMixin, LoginRequiredMixin, TemplateView):
    title = 'Профіль'
    template_name = 'user/index.html'


class TelegramUserListView(TitleMixin, LoginRequiredMixin, ListView):
    model = TelegramUser
    paginate_by = 3
    title = 'Telegram users'
    template_name = 'user/telegram_users/telegram_users_list.html'


class TelegramUserDetailView(TitleMixin, LoginRequiredMixin, GroupRequiredMixin, DetailView):
    model = TelegramUser
    title = 'Telegram user detail'
    template_name = 'user/telegram_users/telegram_user_detail.html'
    group_required = 'manager'


class TelegramUserCreateView(TitleMixin, LoginRequiredMixin, GroupRequiredMixin, CreateView):
    model = TelegramUser
    form_class = TelegramUserForm
    title = 'Create Telegram user'
    template_name = 'user/telegram_users/telegram_user_create.html'
    success_url = reverse_lazy('user:tg_users')
    group_required = 'manager'


class TelegramUserUpdateView(TitleMixin, LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    model = TelegramUser
    form_class = TelegramUserForm
    title = 'Update Telegram user'
    template_name = 'user/telegram_users/telegram_user_update.html'
    success_url = reverse_lazy('user:tg_users')
    group_required = 'manager'


class TelegramUserDeleteView(TitleMixin, LoginRequiredMixin, GroupRequiredMixin, DeleteView):
    model = TelegramUser
    title = 'Delete Telegram user'
    template_name = 'user/telegram_users/telegram_user_delete.html'
    success_url = reverse_lazy('user:tg_users')
    group_required = 'manager'
