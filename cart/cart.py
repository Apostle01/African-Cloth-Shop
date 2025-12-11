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

        # Price as a float for calculations
        price = float(product.price)

        if product_id not in self.cart:
            self.cart[product_id] = {
                "id": product.id,
                "name": product.name,
                "price": price,
                "quantity": quantity,
                "image": product.image.url if product.image else "",
            }
        else:
            self.cart[product_id]["quantity"] += quantity
            self.cart[product_id]["total_price"] = (
                self.cart[product_id]["quantity"] * price
            )

        self.save()

    def update(self, product, quantity):
        product_id = str(product.id)

        if product_id in self.cart:
            price = float(product.price)
            self.cart[product_id]["quantity"] = quantity
            self.cart[product_id]["total_price"] = price * quantity

        self.save()

    def delete(self, product):
        product_id = str(product.id)

        if product_id in self.cart:
            del self.cart[product_id]

        self.save()

    def save(self):
        self.session["cart"] = self.cart
        self.session.modified = True

    def get_total(self):
        total = 0
        for item in self.cart.values():
            price = float(item.get("price", 0))
            qty = int(item.get("quantity", 0))
            total += price * qty
        return total

    def __len__(self):
        return sum(item["quantity"] for item in self.cart.values())

    def get_items(self):
        return self.cart.values()


# from products.models import Product

# class Cart:
#     def __init__(self, request):
#         self.session = request.session
#         cart = self.session.get("cart")

#         if not cart:
#             cart = self.session["cart"] = {}

#         self.cart = cart

#     def add(self, product, quantity=1):
#         product_id = str(product.id)

#         if product_id not in self.cart:
#             self.cart[product_id] = {"quantity": quantity}
#         else:
#             self.cart[product_id]["quantity"] += quantity

#         self.save()

#     def update(self, product, quantity):
#         product_id = str(product.id)

#         if product_id in self.cart:
#             self.cart[product_id]["quantity"] = quantity

#         self.save()

#     def delete(self, product):
#         product_id = str(product.id)

#         if product_id in self.cart:
#             del self.cart[product_id]

#         self.save()

#     def save(self):
#         self.session["cart"] = self.cart
#         self.session.modified = True

#     def get_total(self):
#         total = 0
#         for key, value in self.cart.items():
#             product = Product.objects.get(id=key)
#             total += product.price * value["quantity"]
#         return total

#     def __len__(self):
#         return sum(item["quantity"] for item in self.cart.values())
 