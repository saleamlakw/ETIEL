from django.shortcuts import render,redirect
from .models import *
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required
def home(request):
    women =Catagory.objects.get(name="women")
    women_products = women.products.all()[:2]
    men =Catagory.objects.get(name="men's")
    men_products = men.products.all()[:2]
    kid =Catagory.objects.get(name="kids")
    kid_products = kid.products.all()[:2]
    all=[women_products ,men_products,kid_products]
    all_products=[]
    for catag in all:
        for c in catag:
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
                messages.info(request, 'username is exist ')
                return redirect(register)
            else:
                user = User.objects.create_user(username=username,
                password=password, email=email, first_name=first_name, last_name=last_name)
                user.set_password(password)
                user.save()
                print("success")
                return redirect('login')
    else:
        print("no post method")
        return render(request,'register.html')
def product(request,pk):
    product=get_object_or_404(Product, pk=pk)
    return render(request,'product-centered.html',{"product":product})
def shop(request,shop_pk):
    pro=get_object_or_404(Catagory,pk=shop_pk)
    catagorized_product=pro.products.all()
    return render(request,'shop.html',{"catagorized_product":catagorized_product,"catagory_name":pro.name})
@login_required
def myAccount(request):
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
            print(username)
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
        user= User.objects.get(username=request.user)
        return render(request,'myAccount.html',{"user":user})
def _cart_id(request):
    cart=request.session.session_key
    if not cart:
        cart=request.session.create()
    return cart
def add_cart(request,product_id):
    current_user=request.user
    if current_user.is_authenticated:
        product=get_object_or_404(Product, pk=product_id)
        # try:
        #     cart=Cart.objects.get(cart_id=_cart_id(request))
        # except Cart.DoesNotExist:
        #     cart=Cart.objects.create(
        #         cart_id=_cart_id(request)
        #     )
        # cart.save()
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

