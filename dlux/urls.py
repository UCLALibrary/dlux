"""URLs for dlux.

These should only include a few utility views like logs and release notes. Most functionality is
accessed via the django admin site.
"""

from django.urls import path

from . import views

urlpatterns = [
    path("logs/", views.show_log, name="show_log"),
    path("logs/<int:line_count>", views.show_log, name="show_log"),
    path("release_notes/", views.release_notes, name="release_notes"),
]
