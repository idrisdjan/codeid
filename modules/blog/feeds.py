from django.contrib.syndication.views import Feed
from django.urls import reverse
from .models import Article

class LatestArticlesFeed(Feed):
    title = "Ваш сайт - последние статьи"
    link = "/feeds/"
    description = "Новые статьи на моем сайте."

    def items(self):
        return Article.objects.order_by('-time_update')[:5]

    def item_title(self, item):
        return item.title # type: ignore

    def item_description(self, item):
        return item.short_description # type: ignore

    def item_link(self, item):
        return reverse('articles_detail', args=[item.slug]) # type: ignore