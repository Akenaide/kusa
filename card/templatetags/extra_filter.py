from django import template

register = template.Library()

def sub(value, arg):
    """
    """
    return arg - value

register.filter('sub', sub)

