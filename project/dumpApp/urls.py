from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='blog-home'),
    path('dump/', views.dump, name='blog-dump'),
    path('about/', views.about, name='blog-about'),
    path('browse/', views.browse, name='blog-browse'),
    path('deals/', views.deals, name='blog-deals'),
    path('order/', views.order, name='blog-order'),
    path('search/', views.search, name='blog-search'),
    path('search_results/', views.search_results, name='blog-search_results'),

]