from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from django.urls import reverse
from django.views.generic import TemplateView, ListView, DetailView, RedirectView
from django.views.generic.edit import CreateView, UpdateView

from ventashop.utils import get_VAT_prices
from ventashop.models import Category, Product, Cart, LineItem, Order


class HomeView(TemplateView):
    template_name = "ventashop/home.html"


class AboutView(TemplateView):
    template_name = "ventashop/about.html"


class ContactView(TemplateView):
    template_name = "ventashop/contact.html"


class ProductView(TemplateView):
    template_name = "ventashop/products.html"


class LoginView(TemplateView):
    template_name = "ventashop/login.html"


class CategoryListView(ListView):
    """Our category list view."""

    model = Category
    paginate_by = 100  # if pagination is desired
    template_name = 'ventashop/categories.html'

    def get_queryset(self):
        """
        Return all categories ordered by name.
        """
        return Category.objects.all().order_by("name")


class ProductListView(ListView):
    """Our product-by-category list view."""

    model = Product
    paginate_by = 100  # if pagination is desired
    template_name = 'ventashop/products.html'
    context_object_name = 'product_list'

    def get_queryset(self, **kwargs):
        """
        Return products by category, ordered by creation date, and with price multiplied by 1000.
        """

        if "slug" in self.kwargs:
            p_set = Product.objects.filter(category__slug=self.kwargs["slug"]).order_by("name")
        else:
            p_set = Product.objects.all().order_by("name")

        for product in p_set:
            product.price *= 1000

        return p_set
    
    def get_context_data(self, **kwargs):
        """
        We also need the list of categories to build our filter.
        """

        context = super().get_context_data(**kwargs)
        context["category_list"] = Category.objects.all().order_by("name")
        return context


class ProductDetailView(DetailView):
    """Our product's detailed view."""

    model = Product
    template_name = 'ventashop/product_detail.html'


class CartView(DetailView):
    """The owner's cart view."""

    model = Cart
    template_name = 'ventashop/cart.html'
    context_object_name = "cart"

    def get_context_data(self, **kwargs):
        """Line item list and VAT calulations to be displayed."""

        context =  super().get_context_data(**kwargs)
        context["line_item_list"] = self.get_object().lineitem_set.all()
        return context


class ProductAddToCartView(RedirectView):
    """Add a product (aka a line item) to cart"""
    
    http_method_names = ["post"]
    pattern_name = 'ventashop:product-detail'

    def get_redirect_url(self, *args, **kwargs):
        """Add product to cart and redirect"""

        cart = get_object_or_404(Cart, pk=kwargs["cart_id"])
        product = get_object_or_404(Product, pk=kwargs["product_id"])
        cart.add_line_item(product, 1000)
        
        kwargs = {}
        args=(product.slug,)
        return super().get_redirect_url(*args, **kwargs)


class LineItemUpdateView(RedirectView):
    """Update a line item quantity in cart"""
    
    http_method_names = ["post"]
    pattern_name = 'ventashop:cart'

    def post(self, request, *args, **kwargs):
        """update quantity, checking its value"""

        if "quantity" in request.POST:
            try:
                quantity = int(request.POST["quantity"])
            except:
                quantity = 1000
        
            if quantity >= 1000:
                cart = get_object_or_404(Cart, pk=kwargs["cart_id"])
                line_item = get_object_or_404(LineItem, pk=kwargs["line_item_id"])
                cart.update_line_item(line_item.product, quantity)
        
        return super().post(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        """Redirect to cart view."""

        # return super().get_redirect_url(*args, kwargs["cart_id"])
        args=(kwargs["cart_id"],)
        kwargs = {}
        return super().get_redirect_url(*args, **kwargs)
    

class LineItemRemoveFromCartView(RedirectView):
    """Remove a line item (aka a product) from cart"""
    
    http_method_names = ["post"]
    pattern_name = 'ventashop:cart'

    def get_redirect_url(self, *args, **kwargs):
        """Delete line item and redirect to cart view"""

        line_item = get_object_or_404(LineItem, pk=kwargs["line_item_id"])
        cart = line_item.cart
        line_item.delete()
        cart.save()
        
        kwargs = {}
        kwargs["cart_id"] = cart.id
        return super().get_redirect_url(*args, kwargs["cart_id"])


class CartEmptyView(RedirectView):
    """Remove all line items (aka products) from cart"""
    http_method_names = ["post"]
    pattern_name = 'ventashop:products-all'

    def get_redirect_url(self, *args, **kwargs):
        """Empty cart"""
        
        cart = get_object_or_404(Cart, pk=kwargs["pk"])
        cart.empty_cart()
        
        kwargs = {}
        return super().get_redirect_url(*args, **kwargs)


#######################
##### ORDER Views #####
#######################


class MakeOrderView(RedirectView):
    """Make order from cart."""

    http_method_names = ["post"]
    pattern_name = 'ventashop:order-detail'

    def get_redirect_url(self, *args, **kwargs):
        """Make order."""
        
        cart = get_object_or_404(Cart, pk=kwargs["pk"])
        order = cart.make_order()
        
        kwargs = {}
        args=(order.slug,)
        return super().get_redirect_url(*args, **kwargs)   


class OrderListView(ListView): 
    """Our order list view."""

    model = Order
    paginate_by = 100  # if pagination is desired
    template_name = 'ventashop/orders.html'
    context_object_name = 'order_list'

    def get_queryset(self):
        """
        Return all orders (ordered in model by date_created),
        for an owner (aka CustomerAccount)
        """
        return Order.objects.all()


class OrderDetailView(DetailView):
    """Our order's detailed view."""

    model = Order
    template_name = 'ventashop/order_detail.html'

    def get_context_data(self, **kwargs):
        """Line item list, order status and last comment to be displayed."""

        context =  super().get_context_data(**kwargs)
        order = self.get_object()

        context["line_item_list"] = order.lineitem_set.all()
        
        comments = order.comment_set.all()
        if comments.count() > 0:
            context["comment"] = comments[0]
        else:
            context["comment"] = False
        
        status_tuple_list = [st for st in Order.STATUS_CHOICES if st[0] == order.status]
        context["status"] = status_tuple_list[0][1]

        return context


######################
##### CRUD Views #####
######################

class CategoryCreateView(CreateView):
    """Our view to create a new category."""
    
    model = Category
    fields = ["name"]
    success_url = "/products/"


class ProductCreateView(CreateView):
    """Our view to create a new product."""
    
    model = Product
    fields = ["name", "image", "description", "price", "category"]
    success_url = "/products/"


# We could add classes to update and/or delete Categories and Products.


# For the desktop app, for now !
# class OrderUpdateView(UpdateView):
#     """Our view to update an odrer."""

#     model = Order
#     fields = ["status",]
#     success_url = "/orders/"
