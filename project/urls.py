"""Project-wide URLs.

The primary functionality is via the django admin site, which is mounted at "/".

Other views can be added for simple utilities (e.g., accessing logs or release notes), but should
not be used extensively. Any path defined by the admin site will take precedence over other views
with the same path.
"""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", admin.site.urls),
    path("", include("dlux.urls")),
    # path("accounts/", include("django.contrib.auth.urls")),
]
