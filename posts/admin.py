from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
  list_display = ('title', 'slug', 'author')
  list_display_links = ('title', 'author')
  ordering = ('date_posted', 'title')