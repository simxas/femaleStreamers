from django import template

register = template.Library()

@register.filter(name='underscore')
def underscore(d, k):
    return d.get(k, None)
