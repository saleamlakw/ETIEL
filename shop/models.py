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
class Contact_mod(models.Model):
    name=models.CharField(max_length=200)
    email=models.EmailField(null=True)
    phone=models.CharField(max_length=200)
    subject=models.TextField()
    message=models.TextField()
    def __str__(self):
        return self.name
class Cart(models.Model):
    cart_id=models.CharField(max_length=250,blank=True)
    date_added=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.cart_id
class Cart_item(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,null=True)
    quantity=models.PositiveIntegerField()
    is_active=models.BooleanField(default=True)
    def sub_total(self):
        return self.product.price * self.quantity
    def __str__(self):
        return self.product.name
class Payment(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    payment_id=models.CharField(max_length=200)
    payment_method=models.CharField(max_length=200)
    amount_paid=models.CharField(max_length=200)
    status=models.CharField(max_length=200)
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.payment_id
class Order(models.Model):
    STATUS=(
        ("New","New"),
        ("Accepted","Accepted"),
        ("Completed","Completed"),
        ("Cancelled","Cancelled"),
    )
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    payment=models.ForeignKey(Payment,on_delete=models.SET_NULL,null=True,blank=True)
    order_number=models.CharField(max_length=200)
    first_name=models.CharField(max_length=200)
    last_name=models.CharField(max_length=200)
    phone_number=models.CharField(max_length=50)
    email=models.EmailField()
    address=models.CharField(max_length=200)
    postal_code=models.CharField(max_length=200)
    country=models.CharField(max_length=200)
    city=models.CharField(max_length=200,null=True)
    order_total=models.FloatField()
    tax=models.FloatField()
    status=models.CharField(max_length=200,choices=STATUS,default="New")
    ip=models.CharField(blank=True,max_length=50)
    is_orderd=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    def __str__(self) -> str:
        return self.first_name
class Order_product(models.Model):
   order=models.ForeignKey(Order,on_delete=models.CASCADE)
   payment=models.ForeignKey(Payment,on_delete=models.SET_NULL,null=True,blank=True)
   user=models.ForeignKey(User,on_delete=models.CASCADE)
   product=models.ForeignKey(Product,on_delete=models.CASCADE)
   quantity=models.PositiveIntegerField()
   product_price=models.FloatField()
   ordered=models.BooleanField(default=False)
   created_at=models.DateTimeField(auto_now_add=True)
   updated_at=models.DateTimeField(auto_now=True)
   def sub_total(self):
        return self.product.price * self.quantity
   def __str__(self) -> str:
       return self.product.name


    
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


