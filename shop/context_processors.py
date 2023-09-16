from .models import *
from .views import _cart_id
def my_context_processor(request):
    total_item=0
    catagory=Catagory.objects.all()
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart=Cart.objects.filter(cart_id=_cart_id(request))
            if request.user.is_authenticated:
                cart_items=Cart_item.objects.all().filter(user=request.user)
            else:
                cart_items=Cart_item.objects.all().filter(cart=cart[:1])
            for cart_item in cart_items:
                total_item+=cart_item.quantity
        except Cart.DoesNotExist:
            total_item=0
    return {
                'catagory': catagory,
                'total_item':total_item,
                }