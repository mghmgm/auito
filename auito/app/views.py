from django.views import generic
from django.views.generic import FormView, UpdateView, DeleteView, CreateView
from django.utils import timezone
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.shortcuts import render
from rest_framework import viewsets
from .serializers import PostSerializer, AdSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from datetime import date
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from .models import Post, Ad, Car, Comment, Favorite
from .forms import LoginForm


class PostViewSet(viewsets.ModelViewSet):
    """
    API для запросов на получение данных о Posts
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    # фильтр поисковая строка
    filter_backends = [filters.SearchFilter]
    search_fields = ["title"]

    # фильтр по постам авторизированного юзера
    @action(methods=["GET"], detail=False)
    def filter_by_user(self, request):
        data = Post.objects.filter(author=self.request.user)
        serializer = PostSerializer(data, many=True)
        return Response(serializer.data)

    # поиск по автору (фильтрация по get параметрам в url)
    @action(methods=["GET"], detail=False)
    def search_by_author(self, request):
        author_name = request.query_params.get("author", None)
        if author_name:
            posts = Post.objects.filter(author__username__icontains=author_name)
            serializer = self.get_serializer(posts, many=True)
            return Response(serializer.data)
        return Response({"error": "author parameter is required"}, status=400)
    
    # поиск по автору (фильтрация по именнованным аргументам в url)
    @action(methods=["GET"], detail=False, url_path='author/(?P<author_name>[^/.]+)')
    def search_by_author_arg(self, request, *args, **kwargs):
        author_name = kwargs.get('author_name')
        if author_name:
            posts = Post.objects.filter(author__username__icontains=author_name)
            serializer = PostSerializer(posts, many=True)
            return Response(serializer.data)
        return Response({"error": "Author name is required"}, status=400)

    # запрос с q
    @action(methods=["GET"], detail=False)
    def filtred_posts(self, request):
        author_first = request.query_params.get("author_first", None)
        author_second = request.query_params.get("author_second", None)
        exception_word = request.query_params.get("exception_word", None)
        posts = Post.objects.filter(
            (Q(author__username=author_first) | Q(author__username=author_second))
            & ~Q(title__icontains=exception_word)
        )
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)


class AdViewSet(viewsets.ModelViewSet):
    """
    API для запросов на получение данных о Ads
    """
    queryset = Ad.objects.all()
    serializer_class = AdSerializer

    # апдейт описания
    @action(methods=["POST"], detail=True)
    def update_description(self, request, pk=None):
        ad = self.get_object()
        new_description = request.data.get("description", None)
        if not new_description:
            return Response(
                {"error": "Description is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        ad.description = new_description
        ad.save()
        return Response(
            {"status": "description updated successfully"}, status=status.HTTP_200_OK
        )

    # запрос с q
    @action(methods=["GET"], detail=False)
    def filtred_ads(self, request):
        brand_first = request.query_params.get("brand_first", None)
        brand_second = request.query_params.get("brand_second", None)
        exception_type = request.query_params.get("exception_type", None)
        data = Ad.objects.filter(
            (Q(car__brand=brand_first) | Q(car__brand=brand_second))
            & ~Q(car__body_type__icontains=exception_type)
        )
        serializer = AdSerializer(data, many=True)
        return Response(serializer.data)


class PostsView(generic.ListView):
    """
    View для страницы с Posts
    """
    template_name = "app/posts.html"
    context_object_name = "latest_post_list"

    def get_queryset(self):
        return Post.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")


class PostView(generic.DetailView):
    """
    View для страницы с Post
    """
    model = Post
    template_name = "app/post.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        user = self.request.user
        if user.is_authenticated:
            context["is_favorited"] = Favorite.objects.filter(
                user=user, post=post
            ).exists()
        return context


class AdsView(generic.ListView):
    """
    View для страницы с Ads
    """
    template_name = "app/ads.html"
    context_object_name = "latest_ad_list"

    def get_queryset(self):
        return Ad.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")


class AdView(generic.DetailView):
    """
    View для страницы с Ad
    """
    model = Ad
    template_name = "app/ad.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ad = self.object
        comments_list = Comment.objects.filter(ad=ad)
        context["comments_list"] = comments_list

        return context


class LoginView(FormView):
    """
    View для страницы Login
    """
    template_name = "app/login.html"
    form_class = LoginForm
    success_url = reverse_lazy("app:posts")

    def form_valid(self, form):
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            form.add_error(None, "Неверное имя пользователя или пароль")
            return self.form_invalid(form)


class ProfileView(LoginRequiredMixin, generic.TemplateView):
    """
    View для страницы Profile
    """
    template_name = "app/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        cars_list = Car.objects.filter(owner=user)
        favorites_list = Favorite.objects.filter(user=user)

        context["user"] = user
        context["cars_list"] = cars_list
        context["favorites_list"] = favorites_list

        return context


class CreateAdView(CreateView):
    """
    View для страницы Create Ad
    """
    model = Ad
    fields = ["image", "title", "description"]
    template_name = "app/create.html"
    success_url = reverse_lazy("app:profile")

    def form_valid(self, form):
        form.instance.pub_date = timezone.now()
        form.instance.author = self.request.user
        car_id = self.kwargs["pk"]
        car = Car.objects.get(pk=car_id)
        form.instance.car = car

        return super().form_valid(form)


class UpdateAdView(UpdateView):
    """
    View для страницы Update Ad
    """
    model = Ad
    fields = ["title", "description", "image"]
    template_name = "app/update.html"
    success_url = reverse_lazy("app:profile")


class DeleteAdView(DeleteView):
    """
    View для страницы Delete Ad
    """
    model = Ad
    template_name = "app/delete.html"
    success_url = reverse_lazy("app:profile")


def logout_view(request):
    logout(request)
    return redirect(reverse_lazy("app:posts"))


def error_404_view(request, exception):
    return render(request, "app/404.html")
