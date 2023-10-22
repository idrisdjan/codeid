from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('posts.urls'), name="home"),
    path('register/', user_views.Register.as_view(), name='register'),
    # path('profile/', user_views.profile, name='profile'),
    path('login/', user_views.Login.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

if settings.DEBUG:
    urlpatterns.extend(static("static/", document_root="static"))
    urlpatterns.extend(static("media/", document_root="media"))
    # urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
admin.site.site_header = 'Панель администрирования'