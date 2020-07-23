from django import template
register = template.Library()

@register.filter
def verbose_name(value):
    """Returns models Meta verbose_name"""
    return value._meta.verbose_name.title()

@register.filter
def verbose_name_plural(value):
    """Returns models Meta verbose_name"""
    return value._meta.verbose_name_plural

@register.filter
def str(value):
    """Returns model.__str__() representaion."""
    return value.__str__()
