from django.contrib import admin
from .models import Cart,CartItems,Profile
# Register your models here.
admin.site.register(Cart)
admin.site.register(CartItems)
admin.site.register(Profile)