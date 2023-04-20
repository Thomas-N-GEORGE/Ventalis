from django.urls import path

from ventashop.views import AboutView, ContactView, HomeView, LoginView, ProductView, CategoryCreateView, CategoryListView, ProductDetailView, ProductListView, ProductCreateView, CartView, CartEmptyView, ProductAddToCartView, LineItemRemoveFromCartView, LineItemUpdateView, OrderListView, OrderDetailView, MakeOrderView

from ventashop.message_views import MessageListView, ConversationListView


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

    ###################################
    ##### PRODUCTS AND CATEGORIES #####
    ###################################
    
    # /products/    (all products)
    path("products/", ProductListView.as_view(), name="products-all"),

    # /category/products/   (products filtered by category)
    path("<slug:slug>/products/", ProductListView.as_view(), name="products"),

    # /5/product_detail
    path("<slug:slug>/product_detail/", ProductDetailView.as_view(), name="product-detail"),

    # /product_form
    path("product_form/", ProductCreateView.as_view() , name='product-create'),

    # /categories
    path("categories/", CategoryListView.as_view(), name='categories'),

    # /category_form
    path("category_form/", CategoryCreateView.as_view() , name='category-create'),

    ################
    ##### CART #####
    ################
    
    # /5/cart/
    path("<int:pk>/cart/", CartView.as_view(), name="cart"),

    # Redirect CartEmptyView
    path("<int:pk>/cart_empty/", CartEmptyView.as_view(), name="cart-empty"),

    # Redirect ProductAddToCartView
    path("product_add/<int:cart_id>/<int:product_id>/", ProductAddToCartView.as_view(), name="product-add-to-cart"),
    
    # Redirect LineItemUpdateCartView
    path("line_item_update/<int:cart_id>/<int:line_item_id>/", LineItemUpdateView.as_view(), name="line-item-update"),

    # Redirect LineItemRemoveFromCartView
    path("line_item_remove/<int:line_item_id>/", LineItemRemoveFromCartView.as_view(), name="line-item-remove"),

    # Redirect MakeOrderView
    path("<int:pk>/make_order/", MakeOrderView.as_view(), name="make-order"),
    
    ##################
    ##### ODRERS #####
    ##################

    # /orders
    path("orders/", OrderListView.as_view(), name="orders"),

    # /5/order_detail
    path("<slug:slug>/order_detail/", OrderDetailView.as_view(), name="order-detail"),

    ####################
    ##### MESSAGES #####
    ####################

    # /conversations
    path("conversations/", ConversationListView.as_view(), name="conversations"),
    
    # /3/messages
    path("<int:pk>/messages/", MessageListView.as_view(), name="messages"),
    
    # /3/messages/5 for 5 last messages
    path("<int:pk>/messages/<int:last>", MessageListView.as_view(), name="messages-last"),

]
