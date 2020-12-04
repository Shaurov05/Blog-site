from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def check_char(value):
    print(value)
    if len(value) < 300:
        return ""
    else:
        return "continue reading"
