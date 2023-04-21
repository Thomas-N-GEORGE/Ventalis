"""Our views' test file."""

from django.core import mail
from django.test import Client, TestCase
from django.urls import reverse

from ventashop.models import (Category, Product, LineItem, 
                              Cart, Order, Comment, 
                              Conversation, Message,
                              )


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


class ContactFormViewTestCase(TestCase):
    """Test class for our contact form."""

    def test_contact_form_view_sends_mail(self):
        """Check if post request sends an email, and redirects to "/"."""

        # Arrange.
        c = Client()
        
        # Act.
        response = c.post(
            "/contact/",
            {
                "company": "test_company",
                "last_name": "test_last_name", 
                "first_name": "test_first_name",
                "from_email": "test_from_email@test.com",
                "subject": "test_subject",
                "content": "test_content",
            },
        )

        # Assert.
        self.assertRedirects(response=response, expected_url=reverse('ventashop:home'))
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "test_subject")


class CategoryFormViewTestCase(TestCase):
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


class CartEditingViewsTestCase(TestCase):
    """
    Test class regrouping tests for views modifying cart content,
    e.g. ProductAddToCartView, LineItemUpdateView, LineItemRemoveFromCartView, CartEmptyView.
    """

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

    def test_product_add_to_cart_view(self):
        """Check if product is added to cart and redirection to "product-detail" page afterwards."""

        # Arrange.
        url = "/product_add/" + self.cart_id + "/" + self.product1_id + "/"

        # Act.
        response = self.c.post(reverse("ventashop:product-add-to-cart",
                                        kwargs={'cart_id': self.cart_id, 'product_id': self.product1_id})) 

        # Assert
        self.assertEqual(self.li_count + 1, self.cart.lineitem_set.filter(cart=self.cart).count())
        self.assertRedirects(response=response, 
                            expected_url=reverse("ventashop:product-detail", args=(self.product1.slug,)))
    
    def test_line_item_update_view_with_product_quantity_GE_1000(self):
        """Check cart update and redirection after updating a product quantity in cart."""
    
        # Arrange.
        self.cart.add_line_item(self.product1, 1000)
        line_item = self.cart.lineitem_set.filter(cart=self.cart, product=self.product1_id)[0]

        # Act.
        response = self.c.post(
            reverse("ventashop:line-item-update",
                kwargs={
                    'cart_id': self.cart.pk, 
                    'line_item_id': line_item.pk,
                    }
                ),
            {"quantity": 1234},
        )

        # Assert.
        self.assertRedirects(response=response, 
                            expected_url=reverse("ventashop:cart", args=(self.cart_id,)))
        # self.assertEqual(self.cart.total_price, 4242 * 1500)  # Why does this fail ???
        self.assertEqual(Cart.objects.get(pk=self.cart.pk).total_price, 4242 * 1234)

    def test_line_item_update_view_with_product_quantity_LT_1000(self):
        """Check cart update and redirection after updating a product quantity < 1000 in cart."""
    
        # Arrange.
        self.cart.add_line_item(self.product1, 1000)
        line_item = self.cart.lineitem_set.filter(cart=self.cart, product=self.product1_id)[0]

        # Act.
        response = self.c.post(
            reverse("ventashop:line-item-update",
                kwargs={
                    'cart_id': self.cart.pk, 
                    'line_item_id': line_item.pk,
                    }
                ),
            {"quantity": 999},
        )

        # Assert.
        self.assertRedirects(response=response, 
                            expected_url=reverse("ventashop:cart", args=(self.cart_id,)))
        self.assertEqual(Cart.objects.get(pk=self.cart.pk).total_price, 4242 * 1000)
    
    def test_line_item_update_view_with_no_product_quantity_in_request(self):
        """Check cart update and redirection after updating a product with missing request "quantity" key."""
    
        # Arrange.
        self.cart.add_line_item(self.product1, 1000)
        line_item = self.cart.lineitem_set.filter(cart=self.cart, product=self.product1_id)[0]

        # Act.
        response = self.c.post(
            reverse("ventashop:line-item-update",
                kwargs={
                    'cart_id': self.cart.pk, 
                    'line_item_id': line_item.pk,
                    }
                ),
        )

        # Assert.
        self.assertRedirects(response=response, 
                            expected_url=reverse("ventashop:cart", args=(self.cart_id,)))
        self.assertEqual(Cart.objects.get(pk=self.cart.pk).total_price, 4242 * 1000)

    def test_line_item_remove_from_cart_view(self):
        """Check cart update and redirection after after removing a product from cart."""

        # Arrange.
        cart_tp_init = self.cart.total_price
        self.cart.add_line_item(self.product1, 1000)
        line_item = self.cart.lineitem_set.filter(cart=self.cart, product=self.product1_id)[0]

        # Act.
        response = self.c.post(
            reverse("ventashop:line-item-remove",
                kwargs={
                    'line_item_id': line_item.pk,
                    }
                ),
        )

        # Assert.
        self.assertRedirects(response=response, 
                            expected_url=reverse("ventashop:cart", args=(self.cart_id,)))
        self.assertEqual(Cart.objects.get(pk=self.cart.pk).total_price, cart_tp_init)

    def test_cart_empty_view(self):
        """Check cart update and redirection after emptying cart."""

        # Arrange.
        cart_tp_init = self.cart.total_price
        self.cart.add_line_item(self.product1, 1000)
        line_item = self.cart.lineitem_set.filter(cart=self.cart, product=self.product1_id)[0]

        # Act.
        response = self.c.post(
            reverse("ventashop:cart-empty",
                kwargs={
                    'pk': self.cart.pk,
                    }
                ),
        )

        # Assert.
        self.assertRedirects(response=response, 
                            expected_url=reverse("ventashop:products-all"))
        self.assertEqual(Cart.objects.get(pk=self.cart.pk).total_price, cart_tp_init)


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


class CartViewTestCase(TestCase):
    """Test class for our cart view."""

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


class ConversationListViewTestCase(TestCase):
    """Test class for our conversation list view."""

    def test_conversation_list_view(self):
        """Check if conversations are displayed in view."""

        # Arrange.
        c = Client()
        conv1 = Conversation.objects.create(subject="test1")
        conv2 = Conversation.objects.create(subject="test2")

        # Act.
        response = c.get("/conversations/")

        # Assert.
        self.assertContains(response, "test1")
        self.assertContains(response, "test2")


class MessageListViewTestCase(TestCase):
    """Test class for our message list view."""

    @classmethod
    def setUpTestData(cls) -> None:
        """Arrange."""

        cls.c = Client()
        cls.conversation = Conversation.objects.create(subject="test")
        cls.conv_id = cls.conversation.pk
        
        # create 10 messages in cls.conversation
        for i in range(0, 10):
            Message.objects.create(
                author="author" + str(i),
                content="content" + str(i),
                conversation=cls.conversation,
            )
    
    def test_display_all_messages(self):
        """Check if all messages are displayed in url "ventashop:messages"."""

        # Arrange.
        url = "/" + str(self.conv_id) + "/messages/"
    
        # Act.
        response = self.c.get(url)

        # Arrange.
        for i in range(0, 10):
            self.assertContains(response, "author" + str(i))
            self.assertContains(response, "content" + str(i))

    def test_display_only_n_messages(self):
        """Check if only the last n messages are displayed in url "ventashop:messages-last"."""

        # Arrange.
        n = 5
        url = "/" + str(self.conv_id) + "/messages/" + str(n)
    
        # Act.
        response = self.c.get(url)

        # Arrange.
        for i in range(0, 5):
            self.assertNotContains(response, "author" + str(i))
            self.assertNotContains(response, "content" + str(i))
            self.assertContains(response, "author" + str(i + 5))
            self.assertContains(response, "content" + str(i + 5))

    def test_new_message_form_in_view(self):
        """
        Check if new message is created with form, 
        and redirection to url "ventashop:messages".
        """

        # Arrange.
        # url = "/" + str(self.conv_id) + "/messages/" + str(n)

        # Act.
        response = self.c.post(
            reverse(
                "ventashop:messages",
                kwargs={"pk": self.conv_id,},
            ),
            {"author": "author11", "content": "content11"},
        )

        # Assert.
        last_message = list(self.conversation.message_set.all())[-1]
        self.assertEqual(last_message.author, "Tom")     # "Tom" as hardcoded author for now in view.
        # self.assertEqual(last_message.author, "author11")     # Needs user mechanism, not yet implemented.
        self.assertEqual(last_message.content, "content11")

        self.assertRedirects(response=response,
                             expected_url=reverse("ventashop:messages-last", args=(self.conv_id, 5,))
        )
