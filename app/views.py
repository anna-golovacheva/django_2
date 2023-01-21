from django.shortcuts import render

from django.shortcuts import render

from app.models import Product


def all_products(request):
    products = Product.objects.order_by('created_date')[:5]
    for product in products:
        print(product)
    context = {
        'object_list': products
    }
    return render(request, 'app/index.html', context)
