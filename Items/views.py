
from django.shortcuts import render
from .models import Items
from django.http import HttpResponseServerError
# Create your views here.
def Item_detail(request,slug):
  items=Items.objects.get(slug=slug)
  context={'items':items}
  return render(request,'items/item_detail.html',context)

