from django.contrib import admin

from django import forms
from . import models


class NewsAdminForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 10, "cols": 100})
    )

    class Meta:
        model = models.News
        fields = "__all__"


class NewsAdmin(admin.ModelAdmin):
    form = NewsAdminForm
    list_display = (
        "id",
        "title",
        "category",
        "author",
        "created_at",
        "updated_at",
        "is_published",
    )
    list_display_links = ("id", "title", "author")
    search_fields = ("title", "content")
    list_editable = ("is_published",)
    list_filter = ("is_published", "category", "author")


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "title")
    list_display_links = ("id", "title")
    search_fields = ("title",)


admin.site.register(models.News, NewsAdmin)
admin.site.register(models.Category, CategoryAdmin)
