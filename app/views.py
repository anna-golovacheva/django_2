from django.conf import settings
from django.core.mail import send_mail
from django.db import transaction
from django.forms import inlineformset_factory
from django.views.generic import ListView, DetailView, CreateView, UpdateView, \
    DeleteView
from django.shortcuts import render

from app.forms import ProductForm, VersionForm
from app.models import Product, Record, Version
from django.urls import reverse_lazy, reverse


def contacts(request):
    if request.method == 'POST':
        print(request.POST.get('name'))
        print(request.POST.get('email'))
        print(request.POST.get('message'))
    return render(request, 'app/contacts.html')


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('app:index')


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('app:index')


class ProductUpdateWithVersionView(UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('app:index')
    template_name = 'app/product_with_version_form.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        FormSet = inlineformset_factory(self.model, Version, form=VersionForm, extra=1)

        if self.request.method == 'POST':
            formset = FormSet(self.request.POST, instance=self.object)
        else:
            formset = FormSet(instance=self.object)

        context_data['formset'] = formset
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']
        with transaction.atomic():
            if form.is_valid():
                self.object = form.save()
                if formset.is_valid():
                    formset.instance = self.object
                    formset.save()

        return super().form_valid(form)


class ProductListView(ListView):
    model = Product


class ProductDetailView(DetailView):
    model = Product


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('app:index')


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
