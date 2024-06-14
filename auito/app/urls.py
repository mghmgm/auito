from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "app"

urlpatterns = [
    path('', views.PostsView.as_view(), name="posts"),
    path('posts/', views.PostsView.as_view(), name="posts"),
    path("posts/<int:pk>/", views.PostView.as_view(), name="post"),
    path("ads/", views.AdsView.as_view(), name="ads"),
    path("ads/<int:pk>/", views.AdView.as_view(), name="ad"),
    path('login/', views.LoginView.as_view(), name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('profile/', views.ProfileView.as_view(), name="profile"),
    path('<int:pk>/create/', views.CreateAdView.as_view(), name='create'),
    path('<int:pk>/update/', views.UpdateAdView.as_view(), name='update'),
    path('<int:pk>/delete/', views.DeleteAdView.as_view(), name='delete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)