from apps.user.models import TelegramUser


class TitleMixin:
    title = None

    def get_context_data(self, **kwargs):
        context = super(TitleMixin, self).get_context_data()
        context['title'] = self.title
        return context


class TelegramUserMixin:
    tg_user: TelegramUser = None

    def get_context_data(self, **kwargs):
        context = super(TelegramUserMixin, self).get_context_data()
        context['tg_user'] = TelegramUser.objects.get(telegram_id=self.request.user.socialaccount_set.get().uid)
        return context
