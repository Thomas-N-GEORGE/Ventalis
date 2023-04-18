from django.urls import path

from ventashop.views import AboutView, ContactView, HomeView, LoginView, ProductView, CategoryCreateView, CategoryListView, ProductDetailView, ProductListView, ProductCreateView, CartView, ProductAddToCartView, LineItemRemoveFromCartView, LineItemUpdateView


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
    
    # /products/    (all products)
    path("products/", ProductListView.as_view(), name="products-all"),

    # /category/products/   (products filtered by category)
    path("<str:category>/products/", ProductListView.as_view(), name="products"),

    # /5/product_detail
    path("<int:pk>/product_detail/", ProductDetailView.as_view(), name="product-detail"),

    # /product_form
    path("product_form/", ProductCreateView.as_view() , name='product-create'),

    # /categories
    path("categories/", CategoryListView.as_view(), name='categories'),

    # /category_form
    path("category_form/", CategoryCreateView.as_view() , name='category-create'),
    
    # /5/cart/
    path("<int:pk>/cart/", CartView.as_view(), name="cart"),

    # ProductAddToCartView
    path("product_add/<int:cart_id>/<int:product_id>/", ProductAddToCartView.as_view(), name="product-add-to-cart"),
    
    # LineItemUpdateCartView
    path("line_item_update/<int:cart_id>/<int:line_item_id>/", LineItemUpdateView.as_view(), name="line-item-update"),

    # LineItemRemoveFromCartView
    path("line_item_remove/<int:line_item_id>/", LineItemRemoveFromCartView.as_view(), name="line-item-remove"),
]
