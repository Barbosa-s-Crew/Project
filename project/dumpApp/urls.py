from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dump/', views.dump, name='dump'),
    path('about/', views.about, name='about'),
    path('browse/', views.browse, name='browse'),
    path('deals/', views.deals, name='deals'),
    path('order/', views.order, name='order'),
    path('search/', views.search, name='search'),
    path('search_results/', views.search_results, name='search_results'),
    path('shopping_cart/', views.shopping_cart, name='shopping_cart'),
 	path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('login_error/', views.login_error, name='login_error'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout, name='logout'),
    path('restaurants/', views.restaurants, name='restaurants'),
    path('item/', views.item, name='item'),
    #path('shopping_cart/', views.shopping_cart, name='shopping_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('checkout_success/', views.checkout_success, name='checkout_success'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
