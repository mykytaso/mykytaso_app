from datetime import timedelta

from django import template

register = template.Library()


@register.filter(name="email_username")
def email_username(value):
    return value.split("@")[0].capitalize()


@register.filter
def minus_hours(value, hours):
    return value - timedelta(hours=int(hours))
