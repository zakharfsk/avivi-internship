from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.views import LoginView
from django.core.handlers.wsgi import WSGIRequest
from django.urls import reverse_lazy
from django_dump_die.middleware import dd, dump

from .forms import UserLoginForm, UserRegistrationForm
from django.views.generic import CreateView, TemplateView

from common.mixins import TelegramUserMixin, TitleMixin
from .models import TelegramUser, User


class UserLoginView(TitleMixin, LoginView):
    title = 'Авторизація'
    form_class = UserLoginForm
    success_url = reverse_lazy('index')
    template_name = 'user/login.html'


class UserRegistrationCreateView(TitleMixin, CreateView):
    title = 'Реєстрація'
    model = User
    form_class = UserRegistrationForm
    success_url = reverse_lazy('user:login')
    template_name = 'user/register.html'


class UserProfileView(TitleMixin, TelegramUserMixin, TemplateView):
    title = 'Профіль'
    tg_user = None
    template_name = 'user/index.html'

    def dispatch(self, request: WSGIRequest, *args, **kwargs):
        dd(request)
        if request.session.get('account_authentication_methods')[0].get('provider') == 'telegram':
            print('telegram')
            social_user = SocialAccount.objects.get(user=request.user)
            TelegramUser.objects.get_or_create(
                telegram_id=social_user.uid,
                username=social_user.extra_data.get('username', ''),
                first_name=social_user.extra_data.get('first_name', ''),
                last_name=social_user.extra_data.get('last_name', ''),
                lang=social_user.extra_data.get('lang', '')
            )
        return super().dispatch(request, *args, **kwargs)
