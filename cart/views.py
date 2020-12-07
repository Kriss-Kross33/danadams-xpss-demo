from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, get_object_or_404
from .forms import AddProductForms
from .cart import Cart
from inventory.models import Product
# from coupons.forms import CouponForm

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = AddProductForms(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'],
                 update_quantity=cd['update'])
    return redirect('cart:cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = AddProductForms(
            initial={'quantity': item['quantity'],
                     'update': True}
        )
    # coupon_form = CouponForm()
    return render(request, 'cart/detail.html', {'cart': cart}),
                                                # 'coupon_form': coupon_form})

