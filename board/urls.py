from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home', views.index, name='home'),
    path('postlist', views.postlist, name='postlist'),
    path('postdetail', views.postdetail, name='postdetail'),
    path('postcreate', views.postcreate, name='postcreate'),
]
