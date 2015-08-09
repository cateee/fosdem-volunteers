from django import template

register = template.Library()

@register.filter
def get_item(container, key):
    try:
        return container[key]
    except (KeyError, IndexError):
        try:
            return container[int(key)]
        except (KeyError, IndexError, ValueError):
            return None
