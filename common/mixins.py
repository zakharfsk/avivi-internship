from django.http import HttpResponseForbidden


class TitleMixin:
    title: str | None = None

    def get_context_data(self, **kwargs):
        context = super(TitleMixin, self).get_context_data()
        context['title'] = self.title
        return context


class GroupRequiredMixin:
    group_required: str | None = None

    def dispatch(self, request, *args, **kwargs):
        if request.user.groups.filter(name=self.group_required.capitalize()).exists():
            return super(GroupRequiredMixin, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseForbidden('Forbidden. You are not in the group required.')
