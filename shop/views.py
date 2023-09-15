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
def cart(request):
    return render(request,'cart.html')
def checkout(request):
    return render(request,'checkout.html')
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