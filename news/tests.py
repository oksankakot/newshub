from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from .models import Category, News
from news.forms import UserLoginForm, UserRegisterForm

from django.contrib.auth.forms import AuthenticationForm


class NewsModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create_user(username="testuser", password="12345")
        test_user.save()

        test_category = Category.objects.create(title="Test Category")
        test_category.save()

        test_news = News.objects.create(
            title="Test News",
            content="This is a test news content",
            photo="photos/test.jpg",
            category=test_category,
            author=test_user,
        )

    def test_get_absolute_url(self):
        news = News.objects.get(id=1)
        self.assertEqual(news.get_absolute_url(), "/news/1/")


class CategoryModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Category.objects.create(title="Test Category")

    def test_get_absolute_url(self):
        category = Category.objects.get(id=1)
        self.assertEqual(category.get_absolute_url(), "/category/1/")


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.home_url = reverse("home")

        self.user = User.objects.create_user(username="testuser", password="12345")

        self.category = Category.objects.create(title="Test Category")

        self.news = News.objects.create(
            title="Test News",
            content="This is a test news content",
            photo="photos/test.jpg",
            category=self.category,
            author=self.user,
        )

    def test_home_view(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "news/news_list.html")

    def test_category_view(self):
        response = self.client.get(
            reverse("category", kwargs={"category_id": self.category.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "news/list_categories.html")

    def test_news_detail_view(self):
        response = self.client.get(reverse("view_news", kwargs={"pk": self.news.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "news/news_detail.html")

    def test_register_view(self):
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "news/register.html")

    def test_login_view(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "news/login.html")


class TestForms(TestCase):

    def test_user_register_form_valid_data(self):
        form = UserRegisterForm(
            data={
                "username": "testuser",
                "first_name": "Test",
                "last_name": "User",
                "email": "test@example.com",
                "password1": "test12345",
                "password2": "test12345",
            }
        )

        self.assertTrue(form.is_valid())

    def test_user_register_form_invalid_data(self):
        form = UserRegisterForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 6)

    def test_user_login_form_invalid_data(self):
        form = UserLoginForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)
