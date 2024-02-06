from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

from .forms import UserLoginForm, UserRegistrationForm
from django.views.generic import CreateView, TemplateView

from common.mixins import TitleMixin
from .models import User


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


class UserProfileView(TitleMixin, TemplateView):
    title = 'Профіль'
    template_name = 'user/index.html'
