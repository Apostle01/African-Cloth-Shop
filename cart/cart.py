from products.models import Product, Profile

class Cart:
    def __init__(self, request):
        self.session = request.session
        # Get request
        self.request = request
        # Get the current session key if it exists
        cart = self.session.get("cart")

        # Restore cart from DB if user is logged in and session cart is empty
        if not cart and request.user.is_authenticated:
            profile = Profile.objects.filter(user=request.user).first()
            if profile and profile.old_cart:
                cart = profile.old_cart
                self.session["cart"] = cart

        if not cart:
            cart = self.session["cart"] = {}

        self.cart = cart

    def add(self, product, quantity=1):
        product_id = str(product.id)
        price = float(product.price)

        if product_id not in self.cart:
            self.cart[product_id] = {
                "quantity": quantity,
                "price": price,
            }
        else:
            self.cart[product_id]["quantity"] += quantity

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

    def clear(self):
        """Remove cart from session"""
        self.session['cart'] = {}
        self.session.modified = True

    def save(self):
        self.session["cart"] = self.cart
        self.session.modified = True

        if self.request.user.is_authenticated:
            Profile.objects.filter(
                user=self.request.user
            ).update(old_cart=self.cart)
    
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

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = float(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item
