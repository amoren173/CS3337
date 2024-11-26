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
#Cart URLs
    path('cart/', views.cart_view, name='cart_view'),
    path('cart/add/<int:book_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('cart/update/<int:cart_item_id>/', views.update_cart, name='update_cart'),
#Checkout
    path('checkout/', views.checkout, name='checkout'),
    path('order_success/', views.order_success, name='order_success'),
]
