from django.contrib.auth import login, get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.views import generic

from .forms import RegisterForm, UpdateForm
from .models import User


class RegisterView(generic.CreateView):
    form_class = RegisterForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("users:user-detail")

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        login(self.request, user)
        return response


class UserDetailView(generic.TemplateView):
    template_name = "users/user_detail.html"


class UserUpdateView(generic.UpdateView):
    model = User
    form_class = UpdateForm
    template_name = "users/user_detail_update.html"
    success_url = reverse_lazy("users:user-detail")

    def get_object(self, queryset=None):
        return self.request.user


class UserPasswordChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = "users/password_change.html"
    success_url = reverse_lazy("users:user-detail")

    def get_object(self, queryset=None):
        return self.request.user
