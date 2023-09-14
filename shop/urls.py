from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
urlpatterns = [
    path('home/',views.home,name="home"),
    path('about/',views.about,name="about"),
    path('cart/',views.cart,name="cart"),
    path('checkout/',views.checkout,name="checkout"),
    path('contact/',views.contact,name="contact"),
    path('login/',views.login,name="login"),
    path('logout/',views.logout,name="logout"),
    path('register/',views.register,name="register"),
    path('product/<int:pk>/',views.product,name="product"),
    path('shop/<int:shop_pk>',views.shop,name="shop"),
    path('myAccount/',views.myAccount,name="myAccount"),
]