from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("dlux.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("admin/", admin.site.urls),
]
