from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Article


class ArticleSitemap(Sitemap):
    """
    Карта-сайта для статей
    """

    changefreq = 'monthly'
    priority = 0.9
    protocol = 'https'

    def items(self):
        return Article.objects.all()

    def lastmod(self, obj):
        return obj.time_update
    

class StaticSitemap(Sitemap):
    """
    Карта-сайта для статичных страниц
    """

    def items(self):
        return ['feedback', 'home']
    
    def location(self, item):
        return reverse(item)