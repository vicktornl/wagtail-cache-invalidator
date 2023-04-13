from django.dispatch import Signal


class PurgeUrlsFromCacheSignal(Signal):
    """
    arguments:
        - site_id
        - urls
    """

    pass


class PurgePageFromCacheSignal(Signal):
    """
    arguments:
        - page_id
    """

    pass


purge_urls_from_cache = PurgeUrlsFromCacheSignal()
purge_page_from_cache = PurgePageFromCacheSignal()
