from django.conf import settings
from decimal import Decimal
from inventory.models import Product


class Cart(object):
    def __init__(self, request):
        """
        Initialize the cart
        :param request:
        """
        # store the current session
        self.session = request.session
        # get the current cart in session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # if not cart set the cart to an empty dictionary
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        # store the current applied coupon in session

    def add(self, product, quantity=1, update_quantity=False):
        """
        Add a product to a cart or update its quantity
        :param product:
        :param quantity:
        :param update_quantity:
        :return:
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,  'price': str(product.price)}
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        # update the session cart
        self.session[settings.CART_SESSION_ID] = self.cart
        # mark the session as modified to save it
        self.session.modified = True

    def remove(self, product):
        """
        Remove product from cart
        :param product_id:
        :return:
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """
        Iterate over all the items in the cart and retrieve their
        corresponding products from the database
        :return:
        """
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Get the number of items in the cart
        :return:
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """
        Get the total price of the items in the cart
        :return:
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in
                   self.cart.values())

    def clear(self):
        """
        Clear the items in the cart
        :return:
        """
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True


