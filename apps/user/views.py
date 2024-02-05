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
    template_name = 'login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['success_url'] = self.success_url
        return context


class UserRegistrationCreateView(TitleMixin, CreateView):
    title = 'Реєстрація'
    model = User
    form_class = UserRegistrationForm
    success_url = reverse_lazy('user:login')
    template_name = 'register.html'


class UserProfileView(TitleMixin, TemplateView):
    title = 'Профіль'
    template_name = 'index.html'
