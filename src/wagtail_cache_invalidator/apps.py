from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class WagtailCacheInvalidatorAppConfig(AppConfig):
    name = "wagtail_cache_invalidator"
    label = "wagtailcacheinvalidator"
    verbose_name = _("Wagtail cache invalidator")
