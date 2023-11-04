from django.urls import path

from .views import ArticleListView, ArticleDetailView, ArticleByCategoryListView, articles_list, ArticleCreateView, \
    ArticleUpdateView, ArticleDeleteView, CommentCreateView, ArticleByTagListView, ArticleSearchResultView, RatingCreateView, \
    ArticleBySignedUser

urlpatterns = [
    path('', ArticleListView.as_view(), name='home'),
    path('articles/', articles_list, name='articles_by_page'),
    path('articles/create/', ArticleCreateView.as_view(), name='articles_create'),
    path('articles/signed/', ArticleBySignedUser.as_view(), name='articles_by_signed_user'),
    path('articles/<str:slug>/update/', ArticleUpdateView.as_view(), name='articles_update'),
    path('articles/<str:slug>/delete/', ArticleDeleteView.as_view(), name='articles_delete'),
    path('articles/<str:slug>/', ArticleDetailView.as_view(), name='articles_detail'),
    path('articles/<int:pk>/comments/create/', CommentCreateView.as_view(), name='comment_create_view'),
    path('articles/tags/<str:tag>/', ArticleByTagListView.as_view(), name='articles_by_tags'),
    path('category/<str:slug>/', ArticleByCategoryListView.as_view(), name="articles_by_category"),
    path('search/', ArticleSearchResultView.as_view(), name='search'),
    path('rating/', RatingCreateView.as_view(), name='rating'),
]