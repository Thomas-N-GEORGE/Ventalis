from django.urls import path

from ventashop.views import AboutView, ContactView, HomeView, LoginView, ProductView, CategoryCreateView, CategoryListView, ProductDetailView, ProductListView, ProductCreateView


app_name = "ventashop"

urlpatterns = [
    # /
    path("", HomeView.as_view(), name="home"),

    # /about
    path("about/", AboutView.as_view(), name="about"),
    
    # /contact
    path("contact/", ContactView.as_view(), name="contact"),
    
    # /login
    path("login/", LoginView.as_view(), name="login"),
    
    # /category/products/
    path("<str:category>/products/", ProductListView.as_view(), name="products"),

    # /5/product_detail
    path("<int:pk>/product_detail/", ProductDetailView.as_view(), name="product detail"),

    # /product_form
    path("product_form/", ProductCreateView.as_view() , name='new product'),

    # /categories
    path("categories/", CategoryListView.as_view(), name='categories'),

    # /category_form
    path("category_form/", CategoryCreateView.as_view() , name='new category'),
]
