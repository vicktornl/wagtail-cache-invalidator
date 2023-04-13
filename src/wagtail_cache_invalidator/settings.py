from django.conf import settings


def get_setting(name: str, default=None):
    return getattr(settings, "WAGTAIL_CACHE_INVALIDATOR_%s" % name, default)


ASYNC = get_setting("ASYNC", default=False)
