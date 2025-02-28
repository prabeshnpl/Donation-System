from django import template
from django.urls import resolve
register = template.Library()

@register.simple_tag
def is_active(request,url_name):
    match = resolve(request.path_info)
    return 'active' if match.url_name == url_name else ''
 
@register.filter(name='pluralize')
def pluralize(donation):
    return 'donations' if donation > 1 else 'donation'

@register.filter(name='manage_status')
def manage_status(status):
    return 'Details' if status == 'completed' else 'Manage'
