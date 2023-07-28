from django.shortcuts import render
from django.views import View
from Items.models import Category, Items



class Index(View) :
    def get(self, request):
        category = Category.objects.all()
        items = Items.objects.all()
        context = {
            'category' : category,
            'items' : items,
        }
        return render(request, 'home/home.html', context)

class About(View):
    def get(self, request):
         return render(request, 'home/about.html')
    
class Menu(View):
    def get(self, request):
        category = Category.objects.all()
        items = Items.objects.all()
        context = {
            'category' : category,
            'items' : items,
        }
        return render(request, 'home/menu.html', context)

    
class Book(View):
    def get(self, request):
         return render(request, 'home/book.html')
    
def items_search_view(request,):
    if request.method=='GET':
       query_dict=request.GET
       querydict=query_dict.get("searchitem"," ")
       print(querydict)
       if querydict:
            qs = Items.objects.filter(item_name__icontains=querydict)
       else:
            qs = Items.objects.none()  # Return an empty queryset if the search query is empty.
       for q in qs:
          print(q.item_name)
          print(q.slug)
          print(q.image)
          print(q.category)
          print(q.price)
       context={"obj_list":qs}
       print(context)
       return render(request,'items/search.html',context=context)