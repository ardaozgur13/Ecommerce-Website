from store.models import Product, Profile

class Cart():
    def __init__(self, request):
        self.session = request.session
        # Get request
        self.request = request
        # Get the current session key if it exists.
        cart = self.session.get('session_key')

        # If the user is new, no session key
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        # Make sure cart is available on all pages of site.
        self.cart = cart

    def db_add(self, product, quantity):
        product_id = str(product)
        product_qty = str(quantity)

        if product_id in self.cart:
            pass
        else:
            #self.cart[product_id] = {'price: ': str(product.price)}
            self.cart[product_id] = int(product_qty)

        self.session.modified = True

        # Deal with loggen in user
        if self.request.user.is_authenticated:
            # Get the user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # Convert {'3':2,'4':1} to {"3":2,"4":1}
            carty = str(self.cart)
            carty = carty.replace("\'","\"")
            # Save carty to profile model 
            current_user.update(old_cart=str(carty))


    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)

        if product_id in self.cart:
            pass
        else:
            #self.cart[product_id] = {'price: ': str(product.price)}
            self.cart[product_id] = int(product_qty)

        self.session.modified = True

        # Deal with loggen in user
        if self.request.user.is_authenticated:
            # Get the user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # Convert {'3':2,'4':1} to {"3":2,"4":1}
            carty = str(self.cart)
            carty = carty.replace("\'","\"")
            # Save carty to profile model 
            current_user.update(old_cart=str(carty))

    def cart_total(self):
        # Get Product IDs
        product_ids = self.cart.keys()
        # lookup these keys in our product database model
        products = Product.objects.filter(id__in=product_ids)
        # Get quantities
        quantities = self.cart
        # Start counting at 0
        total = 0
        for key,value in quantities.items():
            key = int(key)
            for product in products:
                if product.id == key:
                    if product.is_sale:
                        total = total + (product.sale_price * value)
                    else:
                        total = total + (product.price * value)

        return total

    def __len__(self):
        return len(self.cart)

    def get_prods(self):
        # Get ids from cart
        product_ids = self.cart.keys()
        # Use ids to look up products in database
        products = Product.objects.filter(id__in=product_ids)

        return products
    
    def get_quants(self):
        quantities = self.cart
        return quantities
    
    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)

        # Get Cary
        ourcart = self.cart
        # Update Dictionary/Cart
        ourcart[product_id] = product_qty

        self.session.modified = True

        # Deal with loggen in user
        if self.request.user.is_authenticated:
            # Get the user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # Convert {'3':2,'4':1} to {"3":2,"4":1}
            carty = str(self.cart)
            carty = carty.replace("\'","\"")
            # Save carty to profile model 
            current_user.update(old_cart=str(carty))
        thing = self.cart
        return thing
    
    def delete(self, product):
        product_id = str(product)
        # Delete from dictionary/cart
        if product_id in self.cart:
            del self.cart[product_id]
        
        self.session.modified = True

        # Deal with logged in user
        if self.request.user.is_authenticated:
            # Get the user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # Convert {'3':2,'4':1} to {"3":2,"4":1}
            carty = str(self.cart)
            carty = carty.replace("\'","\"")
            # Save carty to profile model 
            current_user.update(old_cart=str(carty))