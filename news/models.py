from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class News(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    photo = models.ImageField(upload_to="news-images")
    is_published = models.BooleanField(default=True)
    category = models.ForeignKey("Category", on_delete=models.PROTECT, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def get_absolute_url(self):
        return reverse("view_news", kwargs={"pk": self.pk})

    class Meta:
        verbose_name = "News item"
        verbose_name_plural = "News items"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(
        max_length=150, db_index=True, verbose_name="Category title"
    )

    def get_absolute_url(self):
        return reverse("category", kwargs={"category_id": self.pk})

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["title"]

    def __str__(self):
        return self.title
