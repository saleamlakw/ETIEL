from django.shortcuts import render,redirect
from .models import *
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required
import requests
from .forms import Order_Form
import datetime
def home(request):
    women =Catagory.objects.get(name="women")
    women_products = women.products.all()
    men =Catagory.objects.get(name="men's")
    men_products = men.products.all()
    kid =Catagory.objects.get(name="kids")
    kid_products = kid.products.all()
    all=[women_products ,men_products,kid_products]
    all_products=[]

    for catag in all:
        num=0
        for c in catag:
            if c.quantity>0 and num<2:
                num+=1
                all_products.append(c)
    # products=Product.objects.all()
    context={"products":all_products}
    return  render(request,'index-3.html',context)
def about(request):
    return render(request,'about-2.html')
def cart(request,total=0,quantity=0,cart_items=None):
    try:
       
        if request.user.is_authenticated:
            cart_items=Cart_item.objects.all().filter(user=request.user,is_active=True)
        else:
            cart=Cart.objects.get(cart_id=_cart_id(request))
            cart_items=Cart_item.objects.all().filter(cart=cart,is_active=True)
        for cart_item in cart_items:
            total+=(cart_item.product.price*cart_item.quantity)
            quantity+=cart_item.quantity
    except:
        pass
    tax=(2*total)/100
    grand_total=tax+total
    context={
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax':tax,
        'grand_total':grand_total
    }
    return render(request,'cart.html',context)
@login_required(login_url="login")
def checkout(request,total=0,quantity=0,cart_items=None):
    try:
        if request.user.is_authenticated:
            cart_items=Cart_item.objects.all().filter(user=request.user,is_active=True)
        else:
            cart=Cart.objects.get(cart_id=_cart_id(request))
            cart_items=Cart_item.objects.all().filter(cart=cart,is_active=True)
        for cart_item in cart_items:
            total+=(cart_item.product.price*cart_item.quantity)
            quantity+=cart_item.quantity
    except:
        pass
    tax=(2*total)/100
    grand_total=tax+total
    context={
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax':tax,
        'grand_total':grand_total
    }
    return render(request,'checkout.html',context)
def contact(request):
    if request.method=='POST':
        name=request.POST['name']
        phone=request.POST['phone']
        email=request.POST['email']
        subject=request.POST['subject']
        message=request.POST['message']
        mod=Contact_mod()
        mod.name=name
        mod.phone=phone
        mod.email=email
        mod.subject=subject
        mod.message=message
        mod.save()
    return render(request,'contact-2.html')
def login(request):
    if request.method == 'POST':
        username =request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            try:
                cart=Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exist=Cart_item.objects.filter(cart=cart).exists()
                if is_cart_item_exist:
                    cart_item=Cart_item.objects.filter(cart=cart)
                    for item in cart_item:
                        item.user=user
                        item.save()
            except:
                pass
            auth.login(request, user)
            url=request.META.get('HTTP_REFERER')
            
            try:
                query=requests.utils.urlparse(url).query
                
                params=dict(x.split('=') for x in query.split('&'))
              
                if 'next' in params:
                    nextpage=params['next']
                    return redirect(nextpage)
            except:
               return redirect('home')
        else:
            messages.info(request, 'Invalid Username or password')
            return redirect('login')
    else:
        return render(request, 'login.html')
def logout(request):
    auth.logout(request)
    return redirect('home')
def register(request):
    if request.method == 'POST':
       username = request.POST['username']
       first_name = request.POST['first_name']
       last_name = request.POST['last_name']
       email = request.POST['email']
       password = request.POST['password']
       Confirm_password = request.POST['Confirm_password']
       if password==Confirm_password:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'username already exist ')
                return redirect(register)
            else:
                user = User.objects.create_user(username=username,
                password=password, email=email, first_name=first_name, last_name=last_name)
                user.set_password(password)
                user.save()
               
                return redirect('login')
       else:
            messages.info(request, 'The new password and the confirmed password are not the same')
    return render(request,'register.html')
def product(request,pk):
    product=get_object_or_404(Product, pk=pk)
    return render(request,'product-centered.html',{"product":product})
def shop(request,shop_pk):
    pro=get_object_or_404(Catagory,pk=shop_pk)
    catagorized_product=pro.products.all()
   
    return render(request,'shop.html',{"catagorized_product":catagorized_product,"catagory_name":pro.name})
@login_required
def myAccount(request,total=0,quantity=0):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username=request.POST.get('username')
        cur_password = request.POST.get('cur_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        # Get the current user
        user = request.user
        # Update user information
        if new_password:
            if cur_password:
                authenticated_user = authenticate(username=request.user.username, password=cur_password)
                if authenticated_user is not None:
                    if confirm_password:
                        if new_password==confirm_password:
                            user.set_password(confirm_password)
                            messages.info(request, "password changed sucessfully")
                        else:
                            messages.info(request, 'The new password and the confirmed password are not the same')
                    else:
                        messages.info(request, 'confirm your password')          
                else:
                    messages.info(request, "you entered incorrect password in current password field")
        if first_name:
            user.first_name=first_name
        if last_name:
            user.last_name=last_name
        if username:
            user.username = username
            
        if email:
            user.email = email
        # Save the updated user to the database
        user.save()
        try:
            auth.login(request,user)
        except:
            print(

                'error'
            )
        # Redirect to a success page or appropriate URL
        return redirect('myAccount')
    else:
        orderdproduct=Order_product.objects.all().filter(user=request.user)
        for item in orderdproduct:
            total+=(item.product.price*item.quantity)
            quantity+=item.quantity
        tax=(2*total)/100
        grand_total=tax+total
        user= User.objects.get(username=request.user)
        return render(request,'myAccount.html',{"user":user,"orderdproduct":orderdproduct,'total':total,'grand_total':grand_total,"quantity":quantity})
def _cart_id(request):
    cart=request.session.session_key
    if not cart:
        cart=request.session.create()
    return cart
def add_cart(request,product_id):
    current_user=request.user
    if current_user.is_authenticated:
        product=get_object_or_404(Product, pk=product_id)
        try:
            cart_item=Cart_item.objects.get(product=product,user=request.user)
            cart_item.quantity+=1
            cart_item.save()
        except Cart_item.DoesNotExist:
            cart_item=Cart_item.objects.create(
                product=product,
                quantity=1,
                user=request.user,
            )
            cart_item.save()
        return redirect('cart')
    else:
        product=get_object_or_404(Product, pk=product_id)
        try:
            cart=Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart=Cart.objects.create(
                cart_id=_cart_id(request)
            )
        cart.save()
        try:
            cart_item=Cart_item.objects.get(product=product,cart=cart)
            cart_item.quantity+=1
            cart_item.save()
        except Cart_item.DoesNotExist:
            cart_item=Cart_item.objects.create(
                product=product,
                quantity=1,
                cart=cart,
            )
            cart_item.save()
        return redirect('cart')
def remove_cart(request,product_id):
    product=get_object_or_404(Product, pk=product_id)
    if request.user.is_authenticated:
        cart_item=Cart_item.objects.get(user=request.user,product=product)
    else:
        cart=Cart.objects.get(cart_id=_cart_id(request))
        cart_item=Cart_item.objects.get(cart=cart,product=product)
    if cart_item.quantity>1:
        cart_item.quantity-=1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')
def remove_cart_item(request,product_id):
    product=get_object_or_404(Product, pk=product_id)
    if request.user.is_authenticated:
        cart_item=Cart_item.objects.get(user=request.user,product=product)
    else:
        cart=Cart.objects.get(cart_id=_cart_id(request))
        cart_item=Cart_item.objects.get(cart=cart,product=product)
    cart_item.delete()
    return redirect('cart')
def place_order(request,total=0,quantity=0):
    current_user=request.user
    cart_item=Cart_item.objects.filter(user=current_user)
    cart_count=cart_item.count()
    if cart_count<=0:
        return redirect('home')
    grand_total=0
    tax=0
    for item in cart_item:
            total+=(item.product.price*item.quantity)
            quantity+=item.quantity
    tax=(2*total)/100
    grand_total=tax+total
    if request.method=='POST':
        form=Order_Form(request.POST)
        if form.is_valid():
            data=Order()
            data.user=current_user
            data.first_name=form.cleaned_data['first_name']
            data.last_name=form.cleaned_data['last_name']
            data.phone_number=form.cleaned_data['phone_number']
            data.email=form.cleaned_data['email']
            data.address=form.cleaned_data['address']
            data.postal_code=form.cleaned_data['postal_code']
            data.country=form.cleaned_data['country']
            data.city=form.cleaned_data['city']
            data.order_total=grand_total
            data.tax=tax
            data.ip=request.META.get('REMOTE_ADDR') 
            data.save()
            #generate order number
            yr=int(datetime.date.today().strftime('%Y'))
            dt=int(datetime.date.today().strftime('%d'))
            mt=int(datetime.date.today().strftime('%m'))
            d=datetime.date(yr,mt,dt)
            current_date=d.strftime("%Y%m%d")
            data.order_number=current_date + str(data.id)
            data.save()
            """moving cart item product to order item product .this must be implemented in payment view
            but since we dont have payment method this fuctionality will excute here"""
            #move the cart item to order product table 
            cart_item=Cart_item.objects.filter(user=request.user)
            for item in cart_item:
                orderproduct=Order_product()
                orderproduct.order_id=data.id
                # orderproduct.payment=Payment
                orderproduct.user_id=request.user.id
                orderproduct.product_id=item.product.id
                orderproduct.quantity=item.quantity
                orderproduct.product_price=item.product.price
                orderproduct.ordered=True
                orderproduct.save()
                #reduce the quantity of the sold product 
                product=Product.objects.get(id=item.product_id)
                product.quantity-=item.quantity
                product.save()
            #clear cart
            Cart_item.objects.filter(user=request.user).delete()
            #send order recived email to the customer 
            #send transaction id and order number back to send datamethod via json response 
            return redirect('success') #this must be to sucess page for now
        else:
            return redirect('checkout')
def success(request):
    return render(request,'success.html')

from django.db.models import Q

def search(request):
    if request.method == 'GET':
        query = request.GET.get('query')
        product=Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
        context = {
            'catagorized_product' : product,
            'query':query
        }
        return render(request,'shop.html', context)