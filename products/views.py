from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect, render, get_object_or_404
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.db.models import Q

from common.views import TitleMixin
from .utils import get_recommended_products
from .models import Basket, Product, ProductCategory, UserSearchLog


class IndexView(TitleMixin, TemplateView):
    template_name = 'products/index.html'
    title = 'Urban-Store'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        return context


class ProductsListView(TitleMixin, ListView):
    model = Product
    template_name = 'products/products.html'
    paginate_by = 3
    title = 'Urban-Store-Каталог'

    def get_queryset(self):
        queryset = super(ProductsListView, self).get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id) if category_id else queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductsListView, self).get_context_data()
        # categories = cache.get('categories')
        # if not categories:
        #     context['categories'] = Product.objects.all()
        #     cache.set('categories', context['categories'], 30)
        # else:
        #     context['categories'] = categories
        context['categories'] = ProductCategory.objects.all()
        return context


@login_required
def basket_add(request, product_id):
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)

    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def product_search(request):
    query = request.GET.get('q')
    products = Product.objects.all()

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        )
        if request.user.is_authenticated:
            UserSearchLog.objects.create(user=request.user, query=query)

    recommended_products = get_recommended_products(request.user)
    return render(request, 'products/product_search.html', {
        'products': products,
        'query': query,
        'recommended_products': recommended_products
    })


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {'product': product}
    return render(request, 'products/product_detail.html', context)
