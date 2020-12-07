from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Category, Product
from cart.forms import AddProductForms
from taggit.models import Tag
from django.http import Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.exceptions import ImproperlyConfigured
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import View
from .forms import AdvancedSearchForm


def index(request):
    products = Product.objects.filter(available=True)
    categories = Category.objects.order_by('name')
    featured_products = Product.featured_products()
    featured_categories = Product.featured_product_categories(4)
    recent_products = Product.recent_products(3)
    return render(request, 'inventory/index.html', {'products': products,
                                                    'categories': categories,
                                                    'featured_products': featured_products,
                                                    'featured_categories': featured_categories,
                                                    'recent_products': recent_products})


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    object_list = Product.availableProducts.all()
    max_product_num = 24
    paginator = Paginator(object_list, max_product_num)   # 24 products per page
    page = request.GET.get('page')  # Get the current page number
    try:
        products = paginator.page(page)
        # products = Product.objects.filter(available=True)

    except PageNotAnInteger:
        # if page number is not an integer deliver the first page
        products = paginator.page(1)
    except EmptyPage:
        # if page index is out of range deliver the last page
        products = paginator.page(paginator.num_pages)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        object_list = Product.availableProducts.filter(category=category)
        paginator = Paginator(object_list, max_product_num)  # 24 products per page
        page = request.GET.get('page')
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            # if page number is not an integer deliver the first page
            products = paginator.page(1)
        except EmptyPage:
            # if page index is out of range deliver the last page
            products = paginator.page(paginator.num_pages)
    return render(request, 'inventory/product/list.html', {'category': category,
                                                           'page': page,
                                                           'categories': categories,
                                                           'products': products})


def product_detail(request, id, slug, tag_slug=None):
    categories = Category.objects.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
    # category = get_object_or_404(Category, slug=slug)
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_form = AddProductForms()
    return render(request,
                  'inventory/product/detail.html',
                  {'categories': categories, 'product': product,
                   'cart_form': cart_form, 'tag': tag})


def product_search(request, page_num):
    form = AdvancedSearchForm(request.GET)
    query = '?' + request.GET.urlencode()
    products = None
    keyword = request.GET.get('keyword', None)
    breadcrumbs = ({'name': 'Search: ' + keyword, 'url': reverse('catalog_search') + query},)

    #if form
    #return render(request, 'inventory/product/search.html')

"""
class OrdersView(generic.ListView):
    template_name = 'inventory/orders.html'
    context_object_name = 'order_list'

    def get_queryset(self):
        return Order.objects.order_by('-created')


class OrderView(generic.DetailView):
    model = Order
    template_name = 'inventory/order.html'

    def get_context_data(self, **kwargs):
        context = super(OrderView, self).get_context_data(**kwargs)
        context['lineitems'] = context['order'].orderitem_set.order_by("item__vendor")
        return context


class ItemView(generic.DetailView):
    model = Product
    template_name = 'inventory/orders/templates/inventory/item.html'

    def get_context_data(self, **kwargs):
        context = super(ItemView, self).get_context_data(**kwargs)
        context['lineitems'] = context['item'].orderitem_set.order_by("order__order_date")
        return context
"""
