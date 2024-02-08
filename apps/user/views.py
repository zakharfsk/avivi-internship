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


class UserProfileView(TitleMixin, TemplateView):
    title = 'Профіль'
    template_name = 'user/index.html'


class ListTelegramUserListView(TitleMixin, ListView):
    model = TelegramUser
    paginate_by = 3
    title = 'Telegram users'
    template_name = 'user/telegram_users/telegram_users_list.html'


class DetailTelegramUserDetailView(TitleMixin, GroupRequiredMixin, DetailView):
    model = TelegramUser
    title = 'Telegram user detail'
    template_name = 'user/telegram_users/telegram_user_detail.html'
    group_required = 'manager'


class CreateTelegramUserCreateView(TitleMixin, GroupRequiredMixin, CreateView):
    model = TelegramUser
    form_class = TelegramUserForm
    title = 'Create Telegram user'
    template_name = 'user/telegram_users/telegram_user_create.html'
    success_url = reverse_lazy('user:tg_users')
    group_required = 'manager'


class UpdateTelegramUserUpdateView(TitleMixin, GroupRequiredMixin, UpdateView):
    model = TelegramUser
    form_class = TelegramUserForm
    title = 'Update Telegram user'
    template_name = 'user/telegram_users/telegram_user_update.html'
    success_url = reverse_lazy('user:tg_users')
    group_required = 'manager'


class DeleteTelegramUserDeleteView(TitleMixin, GroupRequiredMixin, DeleteView):
    model = TelegramUser
    title = 'Delete Telegram user'
    template_name = 'user/telegram_users/telegram_user_delete.html'
    success_url = reverse_lazy('user:tg_users')
    group_required = 'manager'
