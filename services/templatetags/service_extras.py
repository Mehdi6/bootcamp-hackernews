from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def up_to(value, delimiter=None):
    return value.split(delimiter)[0]


up_to.is_safe = True
