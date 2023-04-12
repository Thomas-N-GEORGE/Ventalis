from django.urls import path

from ventashop.views import AboutView, ContactView, HomeView, LoginView, ProductView


app_name = "ventashop"

urlpatterns = [
    # ventashop/
    path("", HomeView.as_view(), name="home"),

    # ventashop/about
    path("about/", AboutView.as_view(), name="about"),
    
    # ventashop/contact
    path("contact/", ContactView.as_view(), name="contact"),
    
    # ventashop/login
    path("login/", LoginView.as_view(), name="login"),
    
    # ventashop/products
    path("products/", ProductView.as_view(), name="products"),
]