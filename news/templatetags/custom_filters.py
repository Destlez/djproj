from django import template

register = template.Library()

cens_ler = [
    'Казино',
    'Деньги',
    'Ниггер',
]
@register.filter()
def cens_word(text):
    for x in cens_ler:
        if x in cens_ler:
            text = text.replace(x,'*' * len(x))
    return text