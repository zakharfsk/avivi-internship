from django import template

from apps.user.models import User

register = template.Library()


@register.filter(name='has_group')
def has_group(user: User, group_name: str):
    return user.groups.filter(name=group_name.capitalize()).exists()
