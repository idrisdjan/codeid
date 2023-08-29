from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('posts.urls'), name="home"),
]

if settings.DEBUG:
    urlpatterns.extend(static("static/", document_root="static"))
    urlpatterns.extend(static("media/", document_root="media"))