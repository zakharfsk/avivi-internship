from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from apps.telegram_support.models import Ticket
from common.mixins import GroupRequiredMixin, TitleMixin


class SupportTicketsListView(TitleMixin, LoginRequiredMixin, GroupRequiredMixin, ListView):
    title = 'Support tickets'
    model = Ticket
    template_name = 'support/tickets_list.html'
    context_object_name = 'tickets'
    group_required = 'manager'
    paginate_by = 10
    ordering = ['-created_at']
