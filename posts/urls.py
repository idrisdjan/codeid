from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostView.as_view(), name='home'),
    path('<int:pk>/', views.PostDetail.as_view()),
]
