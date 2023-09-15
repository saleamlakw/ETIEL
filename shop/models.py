from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your models here.
# class Customer(models.Model):
#     user=models.OneToOneField(User,null=True,blank=True,on_delete=models.CASCADE)
#     phone_number=models.CharField(max_length=200,null=True)
#     address=models.CharField(max_length=200,null=True)
#     def __str__(self) -> str:
#         return self.name
class Catagory(models.Model):
    name=models.CharField(max_length=200)
    def __str__(self):
        return self.name
class Product(models.Model):
    name=models.CharField(max_length=200)
    catagory=models.ForeignKey(Catagory,on_delete=models.CASCADE,related_name="products")
    price=models.DecimalField(max_digits=10,decimal_places=2)
    image=models.ImageField(null=True,blank=True)
    description=models.TextField(null=True)
    created_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)
    quantity=models.PositiveIntegerField()
    def __str__(self):
        return self.name
class Order(models.Model):
    Customer=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    date_ordered=models.DateTimeField(auto_now_add=True)
    update_date=models.DateTimeField(auto_now=True)
    address=models.CharField(max_length=200)
    postal_code=models.CharField(max_length=200)
    # city=models.CharField(max_length=200)
    # complete=models.BooleanField(default=False)#to identify wheather the adding to cart process is complete or not
    # transaction_id=models.CharField(max_length=200,null=True)
    def __str__(self) -> str:
        return self.id
class Order_item(models.Model):
    product=models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    order=models.ForeignKey(Order,on_delete=models.SET_NULL,null=True)
    quantity=models.IntegerField(default=0,null=True,blank=True)
    date_added=models.DateTimeField(auto_now_add=True)
class Contact_mod(models.Model):
    name=models.CharField(max_length=200)
    email=models.EmailField(null=True)
    phone=models.CharField(max_length=200)
    subject=models.TextField()
    message=models.TextField()
    def __str__(self):
        return self.name
# class Shiping_adress(models.Model):
#     customer=models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True)
#     order=models.ForeignKey(Order,on_delete=models.SET_NULL,null=True)
#     country=models.CharField(max_length=200,null=False)
#     phone_number=models.CharField(max_length=200,null=False)
#     address=models.CharField(max_length=200,null=False)
#     city=models.CharField(max_length=200,null=False)
#     state=models.CharField(max_length=200,null=False)
#     zipcode=models.CharField(max_length=200,null=False)
#     date_added=models.DateTimeField(auto_now_add=True)

#     def __str__(self) -> str:
#         return self.address


