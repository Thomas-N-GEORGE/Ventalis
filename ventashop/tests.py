
from decimal import Decimal

from django.test import Client, TestCase
from django.urls import reverse

# Create your tests here.

from ventashop.models import Category, Product, LineItem, Cart, Order, Comment


class StaticViewsTestCase(TestCase):
    """Test class for each of our static views."""

    def setUp(self):
        self.c = Client()

    def test_home(self):
        response = self.c.get("/")
        self.assertContains(response, "Produits de marketing")
    
    def test_about(self):
        response = self.c.get("/about/")
        self.assertContains(response, "Nous sommes une entreprise spécialisée")
    
    # def test_contact(self):
    #     response = self.c.get("/contact/")
    #     self.assertContains(response, "")
    
    # def test_login(self):
    #     response = self.c.get("/login/")
    #     self.assertContains(response, "")
    
    # def test_category(self):
    #     response = self.c.get("/category/")
    #     self.assertContains(response, "")


class CategoryFormTestCase(TestCase):
    """Test class for our Category form."""

    def setUp(self) -> None:
        """Arrange."""

        self.c = Client()
        self.count = Category.objects.all().count()

    def test_category_created(self):
        """Check if new category is written to db."""

        # Act.
        self.c.post("/category_form/", {"name": "test"})

        # Assert
        self.assertEqual(self.count + 1, Category.objects.all().count())
    
    def test_category_unique(self):
        """Check if a category is unique in db."""

        # Act.
        self.c.post("/category_form/", {"name": "test"})
        self.c.post("/category_form/", {"name": "test"})

        # Assert
        self.assertEqual(self.count + 1, Category.objects.all().count())


class ProductCreateViewTestCase(TestCase):
    """Test class for our product create view."""

    @classmethod
    def setUpTestData(cls) -> None:
        """Arrange."""

        cls.c = Client()
        cls.count = Product.objects.all().count()
        cls.category = Category.objects.create(name="test")

    def create_a_product(self):
        """Simple utility method to create a product for test cases."""

        self.c.post(
            "/product_form/", 
            {
                "name": "test", 
                "description": "test description",
                "price": 42.42,
                "category": self.category.id,
            }
        )

    def test_product_created(self):
        """Check if new product is written to db."""

        # Act.
        self.create_a_product()

        # Assert
        self.assertEqual(self.count + 1, Product.objects.all().count())
    
    def test_product_unique(self):
        """Check if a product is unique in db."""

        # Act.
        self.create_a_product()
        self.create_a_product()

        # Assert
        self.assertEqual(self.count + 1, Product.objects.all().count())

    def test_redirect_to_products_all_page_without_category_specified(self):
        """Check redirection to "product-all" page after creating product without category."""

        # Act.
        response = self.c.post(
                "/product_form/", 
                {
                    "name": "test", 
                    "description": "test description",
                    "price": 42.42,
                }
            )
        
        # Assert.
        self.assertRedirects(response=response, 
                             expected_url=reverse("ventashop:products-all"))

    def test_redirect_to_products_all_page_with_category_specified(self):
        """Check redirection to "product-all" page after creating product with category."""

        # Act.
        response = self.c.post(
                "/product_form/", 
                {
                    "name": "test", 
                    "description": "test description",
                    "price": 42.42,
                    "category": self.category.id,
                }
            )
        
        # Assert.
        self.assertRedirects(response=response, 
                             expected_url=reverse("ventashop:products-all"))


class ProductsListViewTestCase(TestCase):
    """Test class for our main product list view."""

    @classmethod
    def setUpTestData(cls) -> None:
        """Arrange."""

        cls.c = Client()
        cls.count = Product.objects.all().count()

        # 2 categories.
        cls.category1 = Category.objects.create(name="test1")
        cls.category2 = Category.objects.create(name="test2")
        
        # 2 products in same category1.
        cls.product1 = Product.objects.create(
            name="product1", 
            description="description1",
            price=4242, 
            category=cls.category1
        )

        cls.product2 = Product.objects.create(
            name="product2", 
            description="description2",
            price=4242, 
            category=cls.category1
        )
    
    def test_product_price_display(self):
        """Check prices multiplied by 1000 are displayed."""

        # Act.
        response = self.c.get("/products/")

        # Assert.
        self.assertContains(response, "4242000")

    def test_all_products_display(self):
        """Check all products are displayed."""

        # Act.
        response = self.c.get("/products/")

        # Assert.
        self.assertContains(response, "product1")
        self.assertContains(response, "product2")

    def test_products_filtered_by_category(self):
        """Check products are displayed in their category."""
        
        # Act.
        url  = "/" + str(self.category1.slug) + "/products/"
        response = self.c.get(url)

        # Assert.
        self.assertContains(response, "product1")
        self.assertContains(response, "product2")
        
    def test_products_filtered_by_category_empty_category(self):
        """Check no products are displayed in "empty" category."""

        # Act.
        url  = "/" + str(self.category2.slug) + "/products/"
        response = self.c.get(url)

        # Assert.
        self.assertNotContains(response, "product1")
        self.assertNotContains(response, "product2")


class ProductAddToCartViewTestCase(TestCase):
    """Test class for our product detail view"""

    @classmethod
    def setUpTestData(cls) -> None:
        """Arrange."""

        cls.c = Client()
        cls.category = Category.objects.create(name="test_cat")
        cls.product1 = Product.objects.create(
            name="product1", 
            description="description1",
            price=4242, 
            category=cls.category 
        )
        cls.cart = Cart.objects.create()

        cls.li_count = cls.cart.lineitem_set.filter(cart=cls.cart).count()
        cls.cart_id = str(cls.cart.pk)
        cls.product1_id = str(cls.product1.pk)

    def test_add_product_to_cart(self):
        """Check if product is added to cart"""

        # Arrange.
        url = "/product_add/" + self.cart_id + "/" + self.product1_id + "/"

        # Act.
        response = self.c.post(reverse("ventashop:product-add-to-cart", 
                                       kwargs={'cart_id': self.cart_id, 'product_id': self.product1_id})) 

        # Assert
        self.assertEqual(self.li_count + 1, self.cart.lineitem_set.filter(cart=self.cart).count())
    
    def test_redirect_to_products_detail_page_after_adding_product(self):
        """Check redirection to "product-detail" page after adding product to cart."""

        # Act.
        response = self.c.post(reverse("ventashop:product-add-to-cart", 
                                       kwargs={'cart_id': self.cart_id, 'product_id': self.product1_id})) 
        
        # Assert.
        self.assertRedirects(response=response, 
                             expected_url=reverse("ventashop:product-detail", args=(self.product1.slug,)))


class ProductDetailViewTestCase(TestCase):
    """Test class for product detail view."""

    @classmethod
    def setUpTestData(cls) -> None:
        """Arrange."""

        cls.c = Client()
        cls.category = Category.objects.create(name="test_cat")
        cls.product1 = Product.objects.create(
            name="product1", 
            description="description1",
            price=4242, 
            category=cls.category 
        )

    def test_display_product_prduct_details(self):
        """Check if every field is displayed in view."""

        # Act.
        response = self.c.get(reverse('ventashop:product-detail', args=(self.product1.slug,)))

        # Assert.
        self.assertContains(response, "product1")
        self.assertContains(response, "description1")
        self.assertContains(response, "4242")
        self.assertContains(response, "test_cat")


class LineItemTest(TestCase):
    """Test class for our Line Item model logic."""

    @classmethod
    def setUpTestData(cls) -> None:
        """Arrange."""

        cls.product1 = Product.objects.create(
            name="product1", 
            description="description1",
            price=4242, 
        )

    def test_line_item_quantity_ge_1000(self):
        """Test to check the quantity field is updated to 1000 if less."""

        # Act.
        li = LineItem.objects.create(product=self.product1, quantity=900)

        # Assert.
        self.assertEqual(li.quantity, 1000)

    def test_line_item_price_create(self):
        """Test to check the price field is populated correctly."""

        # Act.
        li = LineItem.objects.create(product=self.product1, quantity=1000)

        # Assert.
        self.assertEqual(self.product1.price * 1000, li.price)


class CartTestCase(TestCase):
    """Test class for our Cart model logic."""

    @classmethod
    def setUpTestData(cls) -> None:
        """Arrange."""

        cls.product1 = Product.objects.create(
            name="product1", 
            description="description1",
            price=4242, 
        )

        cls.product2 = Product.objects.create(
            name="product2", 
            description="description1",
            price=6789, 
        )

        cls.cart = Cart.objects.create()

    def test_initial_total_price_is_0(self):
        """Initial empty cart total is 0"""

        # Assert.
        self.assertEqual(self.cart.total_price, 0)
        
    def test_add_line_item(self):
        """
        Add a product to cart, 
        check if a relative line item is created,
        check the total price of cart.
        """

        # Arrange.
        li_set_count = LineItem.objects.filter(cart=self.cart).count()

        # Act.
        self.cart.add_line_item(self.product1, 1234)
        li_set = self.cart.lineitem_set.all()

        # Assert.
        self.assertEqual(li_set_count + 1, LineItem.objects.filter(cart=self.cart).count())
        self.assertEqual(self.cart.total_price, self.product1.price * 1234)

    def test_add_line_item_quantity_less_than_1000(self):
        """
        Add a product to cart with quantity less than 1000, 
        check if no relative line item is created,
        check the total price of cart.
        """

        # Arrange.
        li_set_count = LineItem.objects.filter(cart=self.cart).count()

        # Act.
        self.cart.add_line_item(self.product1, 123)

        # Assert.
        self.assertEqual(li_set_count , LineItem.objects.filter(cart=self.cart).count())
        self.assertEqual(self.cart.total_price, 0)
    
    def test_add_same_product_twice_to_cart(self):
        """
        Add a product twice to cart (first with quantity >= 1000, secondly < 1000), 
        check if only a single relative line item is created,
        check the total price of cart.
        """

        # Arrange.
        li_set_count = LineItem.objects.filter(cart=self.cart).count()

        # Act.
        self.cart.add_line_item(self.product1, 1234)
        self.cart.add_line_item(self.product1, 123)

        # Assert.
        self.assertEqual(li_set_count + 1, LineItem.objects.filter(cart=self.cart).count())
        self.assertEqual(self.cart.total_price, self.product1.price * (1234 + 123))

    def test_update_line_item(self):
        """
        Update a product quantity in cart, 
        check if only a single relative line item is created,
        check the total price of cart.
        """

        # Act.
        self.cart.add_line_item(self.product1, 1234)
        self.cart.update_line_item(self.product1, 5678)

        # Assert.
        self.assertEqual(self.cart.total_price, self.product1.price * 5678)
    
    def test_update_line_item_quantity_less_than_1000(self):
        """
        Update a product with quantity < 1000 in cart, 
        check if line item update is aborted.
        """

        # Act.
        self.cart.add_line_item(self.product1, 1234)
        self.cart.update_line_item(self.product1, 123)

        # Assert.
        self.assertEqual(self.cart.total_price, self.product1.price * 1234)

    def test_remove_line_item(self):
        """Check if line item is removed and cart total price updated."""

        # Arrange.
        self.cart.add_line_item(self.product1, 1234)

        li_set = LineItem.objects.filter(cart=self.cart)
        li_set_count = li_set.count()

        # Act.
        self.cart.remove_line_item(li_set[0])

        # Assert.
        self.assertEqual(self.cart.total_price, 0)
        self.assertEqual(LineItem.objects.filter(cart=self.cart).count(), li_set_count - 1)

    def test_empty_cart(self):
        """Check if line items are removed and cart total price reset to 0."""

        # Arrange.
        self.cart.add_line_item(self.product1, 1234)
        self.cart.add_line_item(self.product2, 5678)

        # Act.
        self.cart.empty_cart()

        # Assert.
        self.assertEqual(self.cart.total_price, 0)
        self.assertEqual(LineItem.objects.filter(cart=self.cart).count(), 0)

    def test_calculate_total_price(self):
        """Check for correct total price of cart."""

        # Arrange.
        self.cart.add_line_item(self.product1, 1234)
        self.cart.add_line_item(self.product2, 5678)

        # Act.
        self.cart.calculate_total_price()

        # Assert.
        self.assertEqual(self.cart.total_price, 4242 * 1234 + 6789 * 5678)

    def test_create_order_aborted_if_empty_cart(self):
        """
        Check if order is not created from  an "empty" cart, 
        """

        o_count = Order.objects.all().count()

        # Act.
        self.cart.make_order()

        # Assert.
        self.assertEqual(Order.objects.all().count(), o_count)

    def test_create_order_cart_emptied(self):
        """
        Check if order is created from our cart, 
        check is cart is "emptied", its total price reset to 0.
        """
        
        # Arrange.
        self.cart.add_line_item(self.product1, 1234)
        o_count = Order.objects.all().count()

        # Act.
        self.cart.make_order()

        # Assert.
        self.assertEqual(Order.objects.all().count(), o_count + 1)
        self.assertEqual(self.cart.lineitem_set.all().count(), 0)
        self.assertEqual(self.cart.total_price, 0)
    
    def test_create_order_check_order_is_correctly_populated(self):
        """
        Check created order from our cart has its fields correctly populated : 
        the line items should be passed to the order,
        the total price or the order sould be the same as was cart's.
        """
        
        # Arrange.
        self.cart.add_line_item(self.product1, 1234)
        self.cart.add_line_item(self.product2, 5678)
        cart_tp = self.cart.total_price
        li_list = list(self.cart.lineitem_set.all())

        # Act.
        self.cart.make_order()
        
        # Assert.
        o_set = Order.objects.all()
        order = o_set[o_set.count() - 1]

        self.assertListEqual(list(order.lineitem_set.all()), li_list)
        self.assertEqual(order.total_price, cart_tp)


class CartViewTestCase(TestCase):
    """Test clas for our cart view."""

    @classmethod
    def setUpTestData(cls) -> None:
        """Arrange."""

        cls.product1 = Product.objects.create(
            name="product1", 
            description="description1",
            price=4242, 
        )

        cls.product2 = Product.objects.create(
            name="product2", 
            description="description1",
            price=6789, 
        )

        cls.cart = Cart.objects.create()


class OrderTestCase(TestCase):
    """Test class for our Cart model logic."""

    @classmethod
    def setUpTestData(cls) -> None:
        """Arrange."""

        cls.order = Order.objects.create()

    def test_add_comment(self):
        """Check if comment is created."""

        # Arrange.
        com_count = Comment.objects.all().count()

        # Act.
        self.order.add_comment("test")
        order_comments = self.order.comment_set.all()

        # Assert.
        self.assertEqual(com_count + 1, Comment.objects.all().count())
        self.assertEqual(list(order_comments)[0].content, "test")


class TestComment(TestCase):
    """Test class for our Comment model logic."""

    @classmethod
    def setUpTestData(cls) -> None:
        """Arrange."""

        cls.order = Order.objects.create()

    def test_message_ordering_in_queryset(self):
        """Check if ordering by descending datetime."""

        # Arrange.
        self.order.add_comment("test1")
        self.order.add_comment("test2")
        self.order.add_comment("test3")

        # Act.
        order_comments = self.order.comment_set.all()

        # Assert.
        self.assertTrue(
            order_comments[0].date_created > 
            order_comments[1].date_created > 
            order_comments[2].date_created
        )
