from django.http import JsonResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from taggit.models import Tag
from django.db.models import Count

from .models import Article, Category, Comment, Rating
from .forms import ArticleCreateForm, ArticleUpdateForm, CommentCreateForm
from ..services.utils import get_client_ip
from ..services.mixins import AuthorRequiredMixin

import random


class ArticleListView(ListView):
    model = Article
    template_name = 'blog/articles_list.html'
    context_object_name = 'articles'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        return context


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'blog/articles_detail.html'
    context_object_name = 'article'
    queryset = model.objects.detail() # type: ignore

    def get_similar_articles(self, obj):
        article_tags_ids = obj.tags.values_list('id', flat=True)
        similar_articles = Article.objects.filter(tags__in=article_tags_ids).exclude(id=obj.id)
        similar_articles = similar_articles.annotate(related_tags=Count('tags')).order_by('-related_tags')
        similar_articles_list = list(similar_articles.all())
        random.shuffle(similar_articles_list)
        return similar_articles_list[:6]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.title # type: ignore
        context['form'] = CommentCreateForm
        context['similar_articles'] = self.get_similar_articles(self.object) # type: ignore
        return context


class ArticleByCategoryListView(ListView):
    model = Article
    template_name = 'blog/articles_list.html'
    context_object_name = 'articles'
    category = None

    def get_queryset(self):
        self.category = Category.objects.get(slug=self.kwargs['slug'])
        queryset = Article.objects.all().filter(category__slug=self.category.slug)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Статьи из категории: {self.category.title}' # type: ignore
        return context


class ArticleByTagListView(ListView):
    model = Article
    template_name = 'blog/articles_list.html'
    context_object_name = 'articles'
    paginate_by = 10
    tag = None

    def get_queryset(self):
        self.tag = Tag.objects.get(slug=self.kwargs['tag'])
        queryset = Article.objects.all().filter(tags__slug=self.tag.slug)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Статьи по тегу: {self.tag.name}' # type: ignore
        return context


class ArticleCreateView(LoginRequiredMixin, CreateView):
    """
    Представление: создание материалов на сайте
    """
    model = Article
    template_name = 'blog/articles_create.html'
    form_class = ArticleCreateForm
    login_url = 'home'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавление статьи на сайт'
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return super().form_valid(form)


class ArticleUpdateView(AuthorRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Представление: обновления материала на сайте
    """
    model = Article
    template_name = 'blog/articles_update.html'
    context_object_name = 'article'
    form_class = ArticleUpdateForm
    login_url = 'home'
    success_message = 'Материал был успешно обновлен'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Обновление статьи: {self.object.title}' # type: ignore
        return context
    
    def form_valid(self, form):
        # form.instance.updater = self.request.user
        form.save() # type: ignore
        return super().form_valid(form)


class ArticleDeleteView(AuthorRequiredMixin, DeleteView):
    """
    Представление: удаления материала
    """
    model = Article
    success_url = reverse_lazy('home')
    context_object_name = 'article'
    template_name = 'blog/articles_delete.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Удаление статьи: {self.object.title}' # type: ignore
        return context


def articles_list(request):
    articles = Article.objects.all()
    paginator = Paginator(articles, per_page=2)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)
    context = {'page_obj': page_object}
    return render(request, 'blog/articles_func_list.html', context)


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentCreateForm

    def is_ajax(self):
        return self.request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    def form_invalid(self, form):
        if self.is_ajax():
            return JsonResponse({'error': form.errors}, status=400)
        return super().form_invalid(form)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.article_id = self.kwargs.get('pk')
        comment.author = self.request.user
        comment.parent_id = form.cleaned_data.get('parent')
        comment.save()

        if self.is_ajax():
            return JsonResponse({
                'is_child': comment.is_child_node(),
                'id': comment.id,
                'author': comment.author.username, # type: ignore
                'parent_id': comment.parent_id,
                'time_create': comment.time_create.strftime('%Y-%b-%d %H:%M:%S'),
                'avatar': comment.author.profile.avatar.url, # type: ignore
                'content': comment.content,
                'get_absolute_url': comment.author.profile.get_absolute_url() # type: ignore
            }, status=200)

        return redirect(comment.article.get_absolute_url())

    def handle_no_permission(self):
        return JsonResponse({'error': 'Необходимо авторизоваться для добавления комментариев'}, status=400)



class ArticleSearchResultView(ListView):
    """
    Реализация поиска статей на сайте
    """
    model = Article
    context_object_name = 'articles'
    paginate_by = 10
    allow_empty = True
    template_name = 'blog/articles_list.html'

    def get_queryset(self):
        query = self.request.GET.get('do')
        search_vector = SearchVector('full_description', weight='B') + SearchVector('title', weight='A')
        search_query = SearchQuery(query) # type: ignore
        return (self.model.objects.annotate(rank=SearchRank(search_vector, search_query)).filter(rank__gte=0.3).order_by('-rank')) # type: ignore

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Результаты поиска: {self.request.GET.get("do")}'
        return context


class RatingCreateView(View):
    model = Rating
    
    def post(self, request, *args, **kwargs):
        article_id = request.POST.get('article_id')
        value = int(request.POST.get('value'))
        ip_address = get_client_ip(request)
        user = request.user if request.user.is_authenticated else None
        
        rating, created = self.model.objects.get_or_create(
            article_id=article_id,
            ip_address=ip_address,
            defaults={'value': value, 'user': user},
        )
        
        if not created:
            if rating.value == value:
                rating.delete()
                return JsonResponse({'status': 'deleted', 'rating_sum': rating.article.get_sum_rating()})
            else:
                rating.value = value
                rating.user = user
                rating.save()
                return JsonResponse({'status': 'updated', 'rating_sum': rating.article.get_sum_rating()})
        return JsonResponse({'status': 'created', 'rating_sum': rating.article.get_sum_rating()})


class ArticleBySignedUser(LoginRequiredMixin, ListView):
    """
    Представление, выводящее список статей авторов, на которые подписан текущий пользователь
    """
    model = Article
    template_name = 'blog/articles_list.html'
    context_object_name = 'articles'
    login_url = 'login'
    paginate_by = 10

    def get_queryset(self):
        authors = self.request.user.profile.following.values_list('id', flat=True) # type: ignore
        queryset = self.model.objects.all().filter(author__id__in=authors) # type: ignore
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Статьи авторов' 
        return context