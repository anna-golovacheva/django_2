from django.shortcuts import render

from django.shortcuts import render


def all_products(request):
    return render(request, 'app/index.html')
