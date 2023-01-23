from django import template

register = template.Library()


@register.filter
def mediapath(text):
    return '/media/' + str(text)


@register.simple_tag
def mediapath(text):
    return '/media/' + str(text)
