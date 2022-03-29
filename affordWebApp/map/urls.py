from django.urls import path

from . import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('home', views.home, name='home'),
    path('base', views.base_file, name='base'),
    path('about', views.about, name='about')
]