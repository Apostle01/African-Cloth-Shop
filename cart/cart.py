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

    #========ADD============
    def add(self, product, quantity=1):
        product_id = str(product.id)
        price = float(product.current_price)

        if product_id not in self.cart:
            self.cart[product_id] = {
                "quantity": int(quantity),
                "price": price,
                "product_id": product.id,
                "name": product.name,
                "image": product.image.url if product.image else "",
            }
        else:
            self.cart[product_id]["quantity"] += int(quantity)
            self.cart[product_id]["price"] = price

        self.save()

    #========= UPDATE ===========      
    def update(self, product, quantity):
        product_id = str(product.id)

        if product_id in self.cart:
            price = float(product.current_price)
            quantity = int(quantity)

            self.cart[product_id]["quantity"] = quantity
            self.cart[product_id]["price"] = price
            self.cart[product_id]["total_price"] = price * quantity

        self.save()

    #======= DELETE =========
    def delete(self, product):
        product_id = str(product.id)

        if product_id in self.cart:
            del self.cart[product_id]

        self.save()

    #========= CLEAR ===========
    def clear(self):
        """Remove cart from session"""
        self.session['cart'] = {}
        self.session.modified = True

    #========== SAVE ===========
    def save(self):
        self.session["cart"] = self.cart
        self.session.modified = True

        if self.request.user.is_authenticated:
            Profile.objects.filter(
                user=self.request.user
            ).update(old_cart=self.cart)
    
    #============ TOTAL =========
    def get_total(self):
        total = 0
        
        for product_id, item in self.cart.items():
            try:
                product = Product.objects.get(id=product_id)
                price = float(product.current_price)
            except Product.DoesNotExist:
                price = float(item.get("price", 0))

            total += price * int(item.get("quantity", 1))
        return total

    #========= LENGTH =========
    def __len__(self):
        return sum(item["quantity"] for item in self.cart.values())

    #========= ITEMS FOR TEMPLATE =========
    def get_items(self):
        items = []

        for product_id, item in self.cart.items():

            try:
                # Get fresh product from DB
                product = Product.objects.get(id=product_id)

                # Safe quantity
                quantity = int(item.get("quantity", 1))

                # Fresh price from database
                price = float(product.current_price)

                # Correct subtotal
                subtotal = price * quantity

                # Correct image path
                image_url = ""

                if product.image:
                    image_url = product.image.url

                # Append cleaned item
                items.append({
                    "product": product,
                    "name": product.name,
                    "price": price,
                    "quantity": quantity,
                    "image": image_url,
                    "subtotal": subtotal,
                })

            except Product.DoesNotExist:
                continue

        return items

    #====== ITERATOR ========
    def __iter__(self):
        for item in self.get_items():
            yield item