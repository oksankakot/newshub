from django.urls import path

from django.conf.urls.static import static
from django.conf import settings
from .views import *

urlpatterns = [
    path("register/", register, name="register"),
    path("login/", user_login, name="login"),
    path("logout/", user_logout, name="logout"),
    path("", HomeNews.as_view(), name="home"),
    path("categories/<int:category_id>/", NewsByCategory.as_view(), name="category"),
    path("news/<int:pk>/", ViewNews.as_view(), name="view_news"),
    path("news/add-news/", CreateNews.as_view(), name="add_news"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
