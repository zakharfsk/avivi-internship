from django import forms

from apps.telegram_bot.models import TelegramBot


class TelegramBotForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    token = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = TelegramBot
        fields = ('name', 'token', 'username')
