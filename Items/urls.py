from django.urls import path
from .views import Item_detail

urlpatterns = [
    path('<slug>/', Item_detail, name='item_detail'),
]
    