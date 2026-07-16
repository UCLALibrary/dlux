from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", admin.site.urls),
    path("", include("dlux.urls")),
    # path("accounts/", include("django.contrib.auth.urls")),
]
