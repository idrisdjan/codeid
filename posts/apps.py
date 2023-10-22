from django.apps import AppConfig


class PostsConfig(AppConfig):
    verbose_name = 'Запись'
    verbose_name_plural = 'Записи'
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'posts'
