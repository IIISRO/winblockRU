from django import template

register = template.Library()

@register.filter
def startswith(value, arg):
    """
    Usage: {{ value|startswith:"http" }}
    Returns True if 'value' starts with 'arg'
    """
    try:
        return value.startswith(arg)
    except AttributeError:
        return False
