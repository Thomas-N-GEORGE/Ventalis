from django.http import HttpResponseRedirect
from django.shortcuts import render

from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView

from ventashop.models import Category, Product


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
    """Our category list view."""

    model = Product
    paginate_by = 100  # if pagination is desired
    template_name = 'ventashop/products.html'
    context_object_name = 'product_list'

    def get_queryset(self, **kwargs):
        """
        Return products by category, ordered by creation date, and with price multiplied by 1000.
        """

        if "category" in self.kwargs:
            q_set = Product.objects.filter(category__name=self.kwargs["category"]).order_by("name")
        else:
            q_set = Product.objects.all().order_by("name")

        return q_set
    
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


######################
##### CRUD Views #####
######################

class CategoryCreateView(CreateView):
    """Our view to create a new category"""
    
    model = Category
    fields = ["name"]
    success_url = "/all/products/"


class ProductCreateView(CreateView):
    """Our view to create a new product"""
    
    model = Product
    fields = ["name", "image", "description", "price", "category"]
    success_url = "/all/products"


# We can add classes to update and/or delete Categories and Products.
