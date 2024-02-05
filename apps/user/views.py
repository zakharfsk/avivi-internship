from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.views import LoginView
from django.core.handlers.wsgi import WSGIRequest
from django.urls import reverse_lazy
from django_dump_die.middleware import dd, dump

from .forms import UserLoginForm, UserRegistrationForm
from django.views.generic import CreateView, TemplateView

from common.mixins import TitleMixin
from .models import TelegramUser, User


class UserLoginView(TitleMixin, LoginView):
    title = 'Авторизація'
    form_class = UserLoginForm
    success_url = reverse_lazy('index')
    template_name = 'login.html'


class UserRegistrationCreateView(TitleMixin, CreateView):
    title = 'Реєстрація'
    model = User
    form_class = UserRegistrationForm
    success_url = reverse_lazy('user:login')
    template_name = 'register.html'


class UserProfileView(TitleMixin, TemplateView):
    title = 'Профіль'
    template_name = 'index.html'

    def dispatch(self, request: WSGIRequest, *args, **kwargs):
        # TODO: подивитися як перенаправити кол бек на іншу силку саме при телеграм авторизації там додавати запис в бд
        social_user = SocialAccount.objects.get(user=request.user)
        TelegramUser.objects.get_or_create(
            telegram_id=social_user.uid,
            username=social_user.extra_data.get('username', ''),
            first_name=social_user.extra_data.get('first_name', ''),
            last_name=social_user.extra_data.get('last_name', ''),
            lang=social_user.extra_data.get('lang', '')
        )
        return super().dispatch(request, *args, **kwargs)
