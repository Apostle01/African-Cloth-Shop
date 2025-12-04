from decimal import Decimal
from django.conf import settings
from products.models import Product

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get("cart")
        if not cart:
            cart = self.session["cart"] = {}
        self.cart = cart

    def add(self, product, quantity=1):
        product_id = str(product.id)

        if product_id not in self.cart:
            self.cart[product_id] = {
                "quantity": quantity,
                "price": str(product.price)
            }
        else:
            self.cart[product_id]["quantity"] += quantity

        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        for product in products:
            item = self.cart[str(product.id)]
            item["product"] = product
            item["total_price"] = Decimal(item["price"]) * item["quantity"]
            yield item

    def __len__(self):
        return sum(item["quantity"] for item in self.cart.values())

    def get_total(self):
        return sum(
            Decimal(item["price"]) * item["quantity"]
            for item in self.cart.values()
        )

    def clear(self):
        self.session["cart"] = {}
        self.save()

# class Cart():
#     def __init__(self, request):
#         self.session = request.session

#         #Get the current session key if it exists
#         cart = self.session.get('session_key')

#         # If the user is new, no session key! Create one!
#         if 'session_key' not in request.session:
#             cart = self.session['session_key'] = {}


#         # Make sure cart is available on all pages of site
#         self.cart = cart

#     def add(self, product):
#         product_id = str(product_id)

#         # Logic
#         if product_id in self.cart:
#             pass
#         else:
#             self.cart[product_id] = {'price': str(product.price)}

#         self.session.modified = True
