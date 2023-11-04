from django.contrib import admin

from .models import Profile, Feedback

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
  """
  Админ-панель модели профиля
  """
  list_display = ('user', 'birth_date', 'slug')
  list_display_links = ('user', 'slug')


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    """
    Админ-панель модели профиля
    """
    list_display = ('email', 'ip_address', 'user')
    list_display_links = ('email', 'ip_address')