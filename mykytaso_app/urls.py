from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    # path("admin/", admin.site.urls),
    path("", include("webapp.urls", namespace="webapp")),
    path("", include("users.urls", namespace="users")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
