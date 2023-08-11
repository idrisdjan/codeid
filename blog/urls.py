from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('news.urls')),
]  

if settings.DEBUG:
    # add multiple paths using 'extend()'
    urlpatterns.extend(static("static/", document_root="static"))
    urlpatterns.extend(static("media/", document_root="media"))

    # add a single path using 'append()'
    # urlpatterns.append(path("__debug__/", include(debug_toolbar.urls)))