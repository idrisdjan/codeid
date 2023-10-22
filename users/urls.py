from django.urls import path, include
from users.views import Login, Register

urlpatterns = [
  path('', include('django.contrib.auth.urls')),
  
  path('register/', Register.as_view(), name='register'),
  path('login/', Login.as_view(), name='login'),
]