from django.shortcuts import render
from django.views.generic.base import View
from .models import Post

class PostView(View):
    '''Вывод записи'''
    def get(self, request):
        posts = Post.objects.all()
        return render(request, 'posts/posts.html', {'post_list': posts})
    
class PostDetail(View):
    '''Отдельная страница записи'''
    def get(self, request, pk):
        post = Post.objects.get(id=pk)
        return render(request, 'posts/blog_detail.html', {'post': post})

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
