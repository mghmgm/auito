from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

# Регистрация маршрутов для REST API
router = DefaultRouter()
router.register(r"posts", views.PostViewSet)
router.register(r"ads", views.AdViewSet)

app_name = "app"

urlpatterns = [
    # Существующие маршруты для обычных представлений
    path("", views.PostsView.as_view(), name="posts"),
    path("posts/", views.PostsView.as_view(), name="posts"),
    path("posts/<int:pk>/", views.PostView.as_view(), name="post"),
    path("ads/", views.AdsView.as_view(), name="ads"),
    path("ads/<int:pk>/", views.AdView.as_view(), name="ad"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("<int:pk>/create/", views.CreateAdView.as_view(), name="create"),
    path("<int:pk>/update/", views.UpdateAdView.as_view(), name="update"),
    path("<int:pk>/delete/", views.DeleteAdView.as_view(), name="delete"),
    # Маршруты для API
    path("api/", include(router.urls)),  # Пример URL для API
    path(
        "api/posts/author/<str:author_name>/",
        views.PostViewSet.as_view({"get": "search_by_author"}),
        name="search-by-author",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
