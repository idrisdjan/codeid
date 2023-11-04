from django.contrib import admin

from mptt.admin import DraggableMPTTAdmin
from .models import Category, Article, Comment



@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    """
    Админ-панель модели категорий
    """
    list_display = ('tree_actions', 'indented_title', 'id', 'title', 'slug')
    list_display_links = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}



@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}



@admin.register(Comment)
class CommentAdminPage(DraggableMPTTAdmin):
    """
    Админ-панель модели комментариев
    """
    list_display = ('tree_actions', 'indented_title', 'article', 'author', 'time_create', 'status')
    mptt_level_indent = 2
    list_display_links = ('article',)
    list_filter = ('time_create', 'time_update', 'author')
    list_editable = ('status',)