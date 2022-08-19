from django.apps import apps
from wagtail.core.signals import page_published, page_unpublished

from wagtail_cache_invalidator.utils import purge_page_from_cache


def page_published_signal_handler(instance, **kwargs):
    purge_page_from_cache(instance)


def page_unpublished_signal_handler(instance, **kwargs):
    purge_page_from_cache(instance)


def register_signal_handlers():
    Page = apps.get_model("wagtailcore", "Page")
    indexed_models = [model for model in apps.get_models() if issubclass(model, Page)]

    for model in indexed_models:
        page_published.connect(page_published_signal_handler, sender=model)
        page_unpublished.connect(page_unpublished_signal_handler, sender=model)
