from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

from wagtail_cache_invalidator.signal_handlers import register_signal_handlers


class WagtailCacheInvalidatorAppConfig(AppConfig):
    name = "wagtail_cache_invalidator"
    label = "wagtailcacheinvalidator"
    verbose_name = _("Wagtail cache invalidator")

    def ready(self):
        register_signal_handlers()
