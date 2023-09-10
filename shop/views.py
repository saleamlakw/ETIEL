from django.shortcuts import render
def home(request):
    return  render(request,'index-3.html')
def about(request):
    return render(request,'about-2.html')
def cart(request):
    return render(request,'cart.html')
def checkout(request):
    return render(request,'checkout.html')
def contact(request):
    return render(request,'contact-2.html')
def login(request):
    return render(request,'login.html')
def product(request):
    return render(request,'product-centered.html')
def shop(request):
    return render(request,'shop.html')