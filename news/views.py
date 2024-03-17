from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin

# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# import cloudinary.uploader

from django.views.generic import ListView, DetailView, CreateView
from news.models import News, Category
from .forms import NewsForm, UserRegisterForm, UserLoginForm


def register(request: HttpRequest):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "You have successfully registered")
            return redirect("home")
    else:
        form = UserRegisterForm()
    return render(request, "news/register.html", {"form": form})


def user_login(request: HttpRequest):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
    else:
        form = UserLoginForm()
    return render(request, "news/login.html", {"form": form})


def user_logout(request: HttpRequest):
    logout(request)
    return redirect("login")


class HomeNews(ListView):
    model = News
    context_object_name = "news"
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Main Page"
        return context

    def get_queryset(self):
        return News.objects.filter(is_published=True)


class NewsByCategory(ListView):
    model = News
    context_object_name = "news"
    allow_empty = False

    def get_queryset(self):
        return News.objects.filter(
            category_id=self.kwargs["category_id"], is_published=True
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = Category.objects.get(pk=self.kwargs["category_id"])
        return context


class ViewNews(DetailView):
    model = News
    context_object_name = "news_item"


class CreateNews(LoginRequiredMixin, CreateView):
    form_class = NewsForm
    template_name = "news/add_news.html"
    raise_exception = True

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
