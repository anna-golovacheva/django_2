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


def contacts(request):
    if request.method == 'POST':
        print(request.POST.get('name'))
        print(request.POST.get('email'))
        print(request.POST.get('message'))
    return render(request, 'app/contacts.html')


def product_card(request, pr_id):
    product = Product.objects.get(pk=pr_id)
    context = {'object': product}
    return render(request, 'app/product_card.html', context)

