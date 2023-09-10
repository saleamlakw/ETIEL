from django.urls import path
from . import views
urlpatterns = [
    path('home/',views.home,name="home"),
    path('about/',views.about,name="about"),
    path('cart/',views.cart,name="cart"),
    path('checkout/',views.checkout,name="checkout"),
    path('contact/',views.contact,name="contact"),
    path('login/',views.login,name="login"),
    path('product/',views.product,name="product"),
    path('shop/',views.shop,name="shop"),
]