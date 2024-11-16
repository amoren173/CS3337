from django.urls import path

from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('home',views.index, name='index'),
    path('postbook', views.postbook, name='postbook'),
    path('displaybooks', views.displaybooks, name='displaybooks'),
    path('book_detail/<int:book_id>', views.book_detail, name='book_detail'),
    path('mybooks', views.mybooks, name='mybooks'),
    path('book_delete/<int:book_id>', views.book_delete, name='book_delete'),
    path('aboutus', views.aboutus, name='aboutus'),
    path('searchbook', views.searchbook, name='searchbook'),
    path('book_detail/ratebook/<int:book_id>', views.ratebook, name='ratebook'),
]
