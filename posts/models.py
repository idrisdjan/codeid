from django.db import models
from django.utils import timezone

class Post(models.Model):
    '''Данные о посте'''
    title = models.CharField('Заголовок записи', max_length=250)
    slug = models.SlugField(max_length=250)
    description = models.TextField('Текст записи')
    author = models.CharField('Имя автора', max_length=100)
    img = models.ImageField('Изображение', upload_to='image/%Y')

    def __str__(self):
        return f'{self.title}, {self.author}'
    
    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'
