from django.urls import path
from .views import *


urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('cart/', cart, name='cart'),
    path('add_to_cart/<slug>', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:id>', remove_from_cart, name='remove_from_cart'),
    path('order/<slug>', order, name='order'),
]
