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


class SuperUserRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super(SuperUserRequiredMixin, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseForbidden('Forbidden. You are not a superuser.')


class FilterMixin:
    filterset_class = None

    def get_queryset(self):
        queryset = super(FilterMixin, self).get_queryset()
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return self.filterset.qs.distinct()

    def get_context_data(self, **kwargs):
        context = super(FilterMixin, self).get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context
