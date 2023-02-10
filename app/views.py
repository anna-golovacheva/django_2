from django.conf import settings
from django.contrib.auth.decorators import user_passes_test, \
    permission_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.mail import send_mail
from django.db import transaction
from django.forms import inlineformset_factory
from django.http import HttpResponseForbidden
from django.views.generic import ListView, DetailView, CreateView, UpdateView, \
    DeleteView
from django.shortcuts import render, get_object_or_404, redirect

from app.forms import ProductForm, VersionForm, ProductDescriptionForm, \
    ProductCategoryForm
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

    def form_valid(self, form):
        product = form.save()
        product.user = self.request.user
        product.save()
        return super().form_valid(form)


class ProductUpdateWithVersionView(UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
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

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse('app:product_card', kwargs={'pk': pk})

    def test_func(self):
        product = self.get_object()
        return self.request.user == product.user or self.request.user.has_perm(perm='app.change_product')


class ProductListView(ListView):
    model = Product

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.has_perm('app.set_published'):
            return queryset
        return queryset.filter(is_published='published')


class ProductDetailView(DetailView):
    model = Product

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.is_published or self.request.user.has_perm('app:change_description'):
            return self.object
        raise HttpResponseForbidden


@permission_required('app.set_published')
def change_is_published(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if product.is_published == Product.PUBLISHED:
        product.is_published = Product.NOT_PUBLISHED
    else:
        product.is_published = Product.PUBLISHED
    product.save()
    return redirect(request.META.get('HTTP_REFERER'))


class ProductDescriptionUpdateView(UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductDescriptionForm
    template_name = 'app/product_description.html'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse('app:product_card', kwargs={'pk': pk})

    def test_func(self):
        return self.request.user.has_perm(perm='app.change_description')


class ProductCategoryUpdateView(UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductCategoryForm
    template_name = 'app/product_category.html'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse('app:product_card', kwargs={'pk': pk})

    def test_func(self):
        return self.request.user.has_perm(perm='app.change_category')


class ProductDeleteView(UserPassesTestMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('app:index')

    def test_func(self):
        return self.request.user.has_perm(perm='app.delete_product')


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


