from wagtail.contrib.frontend_cache.utils import (
    purge_page_from_cache as wagtail_purge_page_from_cache,
)
from wagtail.contrib.frontend_cache.utils import (
    purge_urls_from_cache as wagtail_purge_urls_from_cache,
)


def purge_urls_from_cache(site, urls):
    from wagtail_cache_invalidator.models import CacheSettings

    cache_settings = CacheSettings.for_site(site)
    backend_settings = cache_settings.backend_settings

    wagtail_purge_urls_from_cache(urls, backend_settings=backend_settings)


def purge_page_from_cache(page):
    from wagtail_cache_invalidator.models import CacheSettings

    site = page.get_site()
    cache_settings = CacheSettings.for_site(site)
    backend_settings = cache_settings.backend_settings

    if cache_settings.purge_all:
        wagtail_purge_urls_from_cache(["/*"], backend_settings=backend_settings)
    else:
        wagtail_purge_page_from_cache(page, backend_settings=backend_settings)
