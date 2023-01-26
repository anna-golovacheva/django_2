from django.conf import settings
from django.core.mail import send_mail
from django.views.generic import ListView, DetailView, CreateView, UpdateView, \
    DeleteView
from django.shortcuts import render
from app.models import Product, Record
from django.urls import reverse_lazy, reverse


# def all_products(request):
#     products = Product.objects.order_by('created_date')[:5]
#     for product in products:
#         print(product)
#     context = {
#         'object_list': products
#     }
#     return render(request, 'app/product_list.html', context)


class ProductListView(ListView):
    model = Product


def contacts(request):
    if request.method == 'POST':
        print(request.POST.get('name'))
        print(request.POST.get('email'))
        print(request.POST.get('message'))
    return render(request, 'app/contacts.html')


# def product_card(request, pr_id):
#     product = Product.objects.get(pk=pr_id)
#     context = {'object': product}
#     return render(request, 'app/product_detail.html', context)


class ProductDetailView(DetailView):
    model = Product


class RecordListView(ListView):
    model = Record


class RecordCreateView(CreateView):
    model = Record
    fields = ('title', 'content', 'preview', 'published')
    success_url = reverse_lazy('app:records')


class RecordUpdateView(UpdateView):
    model = Record
    fields = ('title', 'content', 'preview', 'published', 'views_count')

    def get_success_url(self):
        slug = self.kwargs['slug']
        return reverse('app:record_card', kwargs={'slug': slug})


class RecordDetailView(DetailView):
    model = Record

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.views_count += 1
        if obj.views_count == 100:
            send_mail(
                subject='Просмотры',
                message=f'Количество просмотров записи {obj.title} достигло 100',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=['annegolovacheva@yandex.ru'],
            )
        obj.save()
        return obj


class RecordDeleteView(DeleteView):
    model = Record
    success_url = reverse_lazy('app:records')
