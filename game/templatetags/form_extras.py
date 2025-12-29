from django import template
register = template.Library()

@register.filter
def get_field(form, field_name):
    return form[field_name]

@register.filter
def get_item(dictionary, key):
    if not dictionary:
        return ''
    return dictionary.get(key) or dictionary.get(key.upper()) or dictionary.get(key.lower())