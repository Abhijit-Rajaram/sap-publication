from django.contrib import admin
from django.urls import include, path
from app import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    # admin page to add books and category
    path('add_book/', views.add_book, name='add_book'),
    path('order_status/', views.order_status, name='order_status'),
    # home page
    path('home/', views.home, name='home'),
    path('mainhome/', views.mainhome, name='mainhome'),
    # single product view
    path('product/<str:isbn>/', views.product, name='product'),
    # ordering the product
    path('buy/', views.buy, name='buy'),
    path('carting/<int:id>/', views.carting, name='carting'),
    path('cart/', views.cart, name='cart'),
    path('addQuantity/', views.addQuantity, name='addQuantity'),
    path('order/', views.order, name='order'),
    
    path('booklist/<str:degree>/<str:department>/<int:semester>/', views.booklist, name='booklist'),
    path('buyBookPage/<str:isbn>/', views.buyBookPage, name='buyBookPage'),
    path('viewBookPage/<str:isbn>/', views.viewBookPage, name='viewBookPage'),
    path('searchbar/', views.searchbar, name='searchbar'),
    path('check_username/', views.check_username, name='check_username'),
# path('payment/', views.payment, name='payment'),
    # path('payment/success/', views.payment_success, name='payment_success'),
]