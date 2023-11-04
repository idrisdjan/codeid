from django import template
from django.db.models import Count
from taggit.models import Tag

from ..models import Comment

register = template.Library()

@register.simple_tag
def popular_tags():
    tags = Tag.objects.annotate(num_times=Count('article')).order_by('-num_times')
    tag_list = list(tags.values('name', 'num_times', 'slug'))
    return tag_list


@register.inclusion_tag('includes/latest_comments.html')
def show_latest_comments(count=5):
    comments = Comment.objects.select_related('author').filter(status='published').order_by('-time_create')[:count]
    return {'comments': comments}