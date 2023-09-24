from django.db import models
from django.utils import timezone

class Post(models.Model):
    '''Данные о посте'''
    title = models.CharField('Заголовок записи', max_length=100)
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')
    description = models.TextField('Текст записи')
    author = models.CharField('Имя автора', max_length=100)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    img = models.ImageField('Изображение', upload_to='image/%Y')

    def __str__(self):
        return f'{self.title}, {self.author}'
    
    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'
        
class Comments(models.Model):
    '''Комментарий'''
    email = models.EmailField()
    name = models.CharField('Имя', max_length=50)
    text_comments = models.TextField('Текст комментария', max_length=2000)
    post = models.ForeignKey(Post, verbose_name='Публикация', on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.name}, {self.post}'
    
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        
        
class Likes(models.Model):
    '''Лайки'''
    ip = models.CharField('IP-адрес',max_length=100)
    pos = models.ForeignKey(Post, verbose_name='Публикация', on_delete=models.CASCADE)