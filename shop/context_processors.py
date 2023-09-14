from .models import *
def my_context_processor(request):
    catagory=Catagory.objects.all()
    return {
        'catagory': catagory,
    }