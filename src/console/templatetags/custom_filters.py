from django import template

register = template.Library()

@register.filter(name='replace_if_empty')
def replace_if_empty(value, replacement="Default Value"):
    return value if value else replacement