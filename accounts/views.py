from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from accounts.models import Profile,Cart,CartItems
from django.conf import settings
from Items.models import Items

# Create your views here.
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('email')
        password = request.POST.get('password')

        user_obj = authenticate(request, username = username, password = password)

        if user_obj is None:
            messages.warning(request, "Invalid username or password")
            return HttpResponseRedirect(request.path_info)
        
        # if not user_obj.profile.is_email_verified:
        #     messages.warning(request, "Account is not verified")
        #     return HttpResponseRedirect(request.path_info)

        login(request,user_obj)
        return redirect('/')
        
    return render(request, "accounts/login.html")

def register_view(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username = email)

        if user_obj.exists() :
            messages.warning(request, "Email is already registered ")
            return HttpResponseRedirect(request.path_info)
        
        user_obj = User.objects.create(
            first_name = first_name,
            last_name = last_name,
            email = email,
            username = email
        )
        user_obj.set_password(password)
        user_obj.save()
        

        
        
        messages.success(request, "A verification email has been sent to your mail")
        return HttpResponseRedirect(request.path_info)


    return render(request, 'accounts/register.html')

def cart(request):
    try:
       cart=Cart.objects.get(user=request.user)
    except:
       cart=None
    cart_items=CartItems.objects.filter(cart=cart)
    context={
        "cart":cart,
        "cartitems":cart_items,
    }

   # for item in cart_items:
   #  print(item.size_variant)
   #  print(item.products.product_images)
   #  if item.size_variant:
   #    updated_price=item.products.product_price_by_size(item.size_variant)
   #  else:
   #    updated_price=item.products.price
   #    print(updated_price)
#    if request.method=='POST':
#     #   coupon=request.POST.get('coupon')
#     #   coupon_obj=Coupon.objects.filter(coupon_code__icontains=coupon)
#       if not coupon_obj:
#          messages.warning(request,'Invalid Coupon')
#          return HttpResponseRedirect(request.path_info)
#       if cart.coupon:
#          messages.warning(request,'Coupon Already Exists')
#          return HttpResponseRedirect(request.path_info)
#       if cart.get_cart_total()<coupon_obj[0].minimum_amount:
#          messages.warning(request,f'total bill must be greater than{coupon_obj[0].minimum_amount}')
#          return HttpResponseRedirect(request.path_info)
#       if coupon_obj[0].is_expired:
#          messages.warning(request,f'COUPON EXPIRED')
#          return HttpResponseRedirect(request.path_info)
#    #    print(updated_price)
    #   if cart.get_cart_total()>coupon_obj[0].minimum_amount:
    #      messages.success(request,'Coupon Applied')
    #      cart.coupon=coupon_obj[0]
    #      cart.save()
#    client=razorpay.Client(auth=(settings.KEY_ID,settings.KEY_SECRET))
#    payment=client.order.create({'amount':cart.get_cart_total(),'currency':'INR','payment_capture':1})
#    cart.razor_pay_order_id=payment['id']
#    cart.save()
#    context['payment']=payment
    return render(request,'accounts/cart.html',context)

def add_to_cart(request,slug):
   user=request.user
   products=Items.objects.get(slug=slug)
   price= products.price
   cart,_=Cart.objects.get_or_create(user=user,is_paid=False)
   cart_item=CartItems.objects.create(cart=cart,products=products)
   cart_item.save()
   return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
   
def remove_from_cart(request,id):
   cart_item=CartItems.objects.get(id=id)
   if cart_item:
      cart_item.delete()
   return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# def remove_coupon(request,cart_item_uid):

#    cart_item=Cart.objects.get(uid=cart_item_uid)
#    cart_item.coupon=None
#    cart_item.save()
#    messages.success(request,'Coupon Removed')
#    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def success(request):
   order_id=request.GET.get('order_id')
   cart=Cart.objects.get(razor_pay_order_id=order_id)
   cart.is_paid(True)
   cart.save()
   return HttpResponse('Payment Success')
    
    



def order(request,slug):
    try:
       cart=Items.objects.get(slug=slug)
    except:
       cart=None
    context={
        "item":cart,
        
    }

    return render(request,'accounts/cart.html',context)

