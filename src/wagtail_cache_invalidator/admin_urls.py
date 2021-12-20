from django.urls import path

from wagtail_cache_invalidator import views

app_name = "wagtailcacheinvalidator"

urlpatterns = [
    path("purge/", views.purge, name="purge"),
]
