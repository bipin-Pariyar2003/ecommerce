from django import template

register=template.Library()

@register.filter
def first_ten_words(desc):
    words=desc.split()
    a=' '.join(words[:10])
    return a+"..."