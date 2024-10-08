from django import template
from datetime import datetime

register = template.Library()

@register.simple_tag()
def tag_date(format_string='%d %b %Y'):
    return datetime.utcnow().strftime(format_string)

@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
   d = context['request'].GET.copy()
   for k, v in kwargs.items():
       d[k] = v
   return d.urlencode()

