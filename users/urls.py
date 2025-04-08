from django.urls import path, include

from .views import UserDetailView, RegisterView

app_name = "users"

urlpatterns = [
    path("accounts/register/", RegisterView.as_view(), name="register"),
    path("accounts/me/", UserDetailView.as_view(), name="user-detail"),
    path("accounts/", include("django.contrib.auth.urls")),
]
