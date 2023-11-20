from django import template
from django.db.models import Count

from women import views
from women.models import *
from women.utils import menu

register = template.Library()


@register.inclusion_tag('women/templates_tags/list_categories.html')
def show_categories(cat_selected=0):
    # cats = Category.objects.all()
    cats = Category.objects.annotate(total=Count('posts')).filter(total__gt=0)
    return {'cats': cats, 'cat_selected': cat_selected}


@register.inclusion_tag('women/templates_tags/list_tags.html')
def show_all_tags():
    tags = TagPost.objects.annotate(total=Count('tags')).filter(total__gt=0)
    return {'tags': tags}


# @register.simple_tag()
# def get_menu():
#     return menu
