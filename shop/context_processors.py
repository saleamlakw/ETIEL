from .models import *
from .views import _cart_id
def my_context_processor(request):
    total_item=0
    catagory=Catagory.objects.all()
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart=Cart.objects.get(cart_id=_cart_id(request))
            cart_items=Cart_item.objects.filter(cart=cart)
            for cart_item in cart_items:
                total_item+=cart_item.quantity
        except Cart.DoesNotExist:
            total_item=0
    return {
                'catagory': catagory,
                'total_item':total_item,
                }