from django.urls import path, include

from .views import UserDetailView, RegisterView, UserUpdateView, UserPasswordChangeView

app_name = "users"

urlpatterns = [
    path("accounts/register/", RegisterView.as_view(), name="register"),
    path("accounts/me/", UserDetailView.as_view(), name="user-detail"),
    path("accounts/me/update/", UserUpdateView.as_view(), name="user-update"),
    path("accounts/me/password_change/", UserPasswordChangeView.as_view(), name="password-change"),
    path("accounts/", include("django.contrib.auth.urls")),
]
