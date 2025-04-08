from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views import generic

from .forms import RegisterForm


class RegisterView(generic.CreateView):
    form_class = RegisterForm
    success_url = reverse_lazy("users:user-detail")
    template_name = "registration/register.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        login(self.request, user)
        return response


class UserDetailView(generic.TemplateView):
    template_name = "users/user_detail.html"
