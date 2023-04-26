from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect


from django.contrib.auth import authenticate, login, logout, password_validation
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView
from django.views.generic import TemplateView, ListView, DetailView, RedirectView, FormView, View
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse

from ventashop.models import Category, Product, Cart, LineItem, Order, User
from ventashop.forms import ContactForm, LoginForm, UserForm, EmployeePwdUpdateForm


class HomeView(TemplateView):
    template_name = "ventashop/home.html"


class AboutView(TemplateView):
    template_name = "ventashop/about.html"


class ContactFormView(FormView):
    """Our contact page form view."""

    template_name = "ventashop/contact.html"
    form_class = ContactForm
    success_url = "/"

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.send_email()
        return super().form_valid(form)

######### NOT USED #############
class LoginPageView(View):
    """Our login page form view."""

    # template_name = "ventashop/login.html"
    # authentication_form = LoginForm
    # success_url = "ventashop:home"

    template_name = 'ventashop/login.html'
    form_class = LoginForm
    
    def get(self, request):
        form = self.form_class()
        message = ''
        return render(request, self.template_name, context={'form': form, 'message': message})
        
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = authenticate(
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect(reverse("ventashop:home"))
        message = 'Login failed!'
        return render(request, self.template_name, context={'form': form, 'message': message})
######### NOT USED #############

#########################
##### USER SPECIFIC #####
#########################

class CustomerPasswordResetView(PasswordResetView):
    """Our Customer Reset password class."""

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            email=form.cleaned_data['email'],
            print ("cleaned_email : ", email)
            user = User.objects.filter(email=email[0])
            test = User.objects.all()
            for t in test:
                print(t, "email = ", t.email)
            
            if user.count() > 0:
                # Password change available only to registrated Customers.
                print (user)
                if user[0].role == "CUSTOMER" :
                    return super().post(request, *args, **kwargs)
            else:
                # Redirect here anyway to avoid leaking info about registered emails.
                return HttpResponseRedirect(reverse('ventashop:password_reset_done'))


class UserSignInFormView(FormView):
    """Our user sing in view."""

    template_name="ventashop/auth/sign-in.html"
    form_class=UserForm
    success_url = "/login"

    def form_valid(self, form):
        """Process to create a new "customer"."""

        form.create_user(role = "CUSTOMER")
        return super().form_valid(form)


class EmployeeCreateFormView(FormView):
    """Our employee creation form view, for administrator."""

    form_class=UserForm
    template_name="ventashop/administration/employee_form.html"
    success_url = "/"

    def form_valid(self, form):
        """Process to create a new "employee"."""
        
        form.create_user(role = "EMPLOYEE")
        return super().form_valid(form)


class EmployeePwdUpdateView(FormView):
    """
    Our employee password update view, for administrator.
    """

    form_class=EmployeePwdUpdateForm
    template_name="ventashop/administration/employee_update_form.html"
    success_url="/administration/employees"

    def form_valid(self, form) :
        """Process to update employee's password."""

        # !!!! password_validation.validate_password ???!!!
        # For all forms !!!!

        form.update_employee_pwd(user_id=self.kwargs["pk"])
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """Employee details and old password to be displayed."""
        
        context = super().get_context_data(**kwargs)
        employee = get_object_or_404(User, pk=self.kwargs["pk"])

        context["employee"] = employee
        return context
    

class EmployeeListView(ListView):
    """Our employee list view."""

    model = User
    template_name="ventashop/administration/employees.html"
    context_object_name = "employee_list"

    def get_queryset(self):
        """Get employee list."""

        employee_list = User.objects.filter(role="EMPLOYEE").order_by("date_joined")
        return employee_list


class MySpaceView(ListView):
    """Main view for customer's "my space"."""
    
    template_name = "ventashop/customer/my_space.html"
    model = Order
    paginate_by = 100  # if pagination is desired
    context_object_name = 'order_list'

    def get_queryset(self):
        """
        Return all orders (ordered in model by date_created),
        for an owner (aka CustomerAccount)
        """
        return Order.objects.filter(customer_account=self.request.user.customeraccount)
    
    def get_context_data(self, **kwargs):
        """Objects to be displayed"""

        context = super().get_context_data(**kwargs)
        user = self.request.user

        related_employee = get_object_or_404(User, reg_number = user.customeraccount.employee_reg)
        context["related_employee"] = related_employee
        
        return context


class IntranetView(TemplateView):
    """Main view for employee's Intranet."""

    template_name = "ventashop/employee/intranet.html"


class CustomerListView(ListView):
    """Employee's related customer list view."""

    model = User
    template_name = "ventashop/employee/customers.html"
    context_object_name = "customer_list"

    def get_queryset(self):
        """Get employee's related customer list."""

        user = self.request.user
        customer_list = User.objects.filter(
            role="CUSTOMER", customeraccount__employee_reg=user.reg_number).order_by("date_joined")
        
        return customer_list
    

###################################
##### PRODUCTS AND CATEGORIES #####
###################################

class ProductCreateView(CreateView):
    """Our view to create a new product."""
    
    model = Product
    fields = ["name", "image", "description", "price", "category"]
    success_url = "/products/"


class ProductView(TemplateView):
    """Our product view."""
    template_name = "ventashop/products.html"



    def get_queryset(self):
        """
        Return all categories ordered by name.
        """
        return Category.objects.all().order_by("name")


class ProductListView(ListView):
    """Our product-by-category list view."""

    model = Product
    # paginate_by = 100  # if pagination is desired
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


class CategoryCreateView(CreateView):
    """Our view to create a new category."""
    
    model = Category
    fields = ["name"]
    success_url = "/products/"


class CategoryListView(ListView):
    """Our category list view."""

    model = Category
    paginate_by = 100  # if pagination is desired
    template_name = 'ventashop/categories.html'


################
##### CART #####
################

class CartView(TemplateView):
    """The owner's cart view."""

    template_name = 'ventashop/cart.html'

    def get_context_data(self, **kwargs):
        """Cart with line item list to be displayed."""

        context =  super().get_context_data(**kwargs)
        cart = get_object_or_404(Cart, customer_account=self.request.user.customeraccount)

        context["cart"] = cart
        context["line_item_list"] = cart.lineitem_set.all()
        return context


class ProductAddToCartView(RedirectView):
    """Add a product (aka a line item) to cart"""
    
    http_method_names = ["post"]
    pattern_name = 'ventashop:product-detail'

    def get_redirect_url(self, *args, **kwargs):
        """Add product to cart and redirect"""

        # cart = get_object_or_404(Cart, pk=kwargs["cart_id"])
        cart = get_object_or_404(Cart, customer_account=self.request.user.customeraccount)
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


#################
##### ORDER #####
#################


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
