from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='blog-home'),
    path('dump/', views.dump, name='blog-dump'),
    path('about/', views.about, name='blog-about')
]