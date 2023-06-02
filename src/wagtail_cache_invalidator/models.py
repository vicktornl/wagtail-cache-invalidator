import uuid

from django.conf import settings
from django.db import models
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import (
    FieldPanel,
    MultiFieldPanel,
    ObjectList,
    TabbedInterface,
)
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.models import Site

from wagtail_cache_invalidator import signals
from wagtail_cache_invalidator.settings import ASYNC
from wagtail_cache_invalidator.utils import purge_urls_from_cache

PURGE_ALL_HELP_TXT = _("Purge all cache for this site when pages are (un)published")


class PurgeCacheSite(Site):
    class Meta:
        proxy = True

    def __str__(self):
        result = self.hostname
        if self.port not in [80, 443]:
            result += ":{}".format(self.port)
        if self.is_default_site:
            result += " [{}]".format(_("default"))
        return result


@register_setting
class CacheSettings(BaseSiteSetting):
    purge_all = models.BooleanField(
        verbose_name=_("purge all"), default=False, help_text=PURGE_ALL_HELP_TXT
    )

    cloudfront_enabled = models.BooleanField(verbose_name=_("enabled"), default=False)
    cloudfront_distribution_id = models.CharField(
        verbose_name=_("distribution ID"), max_length=255
    )

    site_panels = [
        FieldPanel("purge_all"),
    ]

    cloudfront_panels = [
        MultiFieldPanel(
            [
                FieldPanel("cloudfront_enabled"),
                FieldPanel("cloudfront_distribution_id"),
            ]
        )
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(cloudfront_panels, heading=_("CloudFront")),
            ObjectList(site_panels, heading=_("Settings")),
        ]
    )

    class Meta:
        verbose_name = _("Cache")
        verbose_name_plural = _("Cache")

    @property
    def backend_settings(self):
        settings = {}

        # https://docs.wagtail.org/en/stable/reference/contrib/frontendcache.html#amazon-cloudfront
        if self.cloudfront_distribution_id and self.cloudfront_enabled:
            settings["cloudfront"] = {
                "BACKEND": "wagtail.contrib.frontend_cache.backends.CloudfrontBackend",
                "DISTRIBUTION_ID": self.cloudfront_distribution_id,
            }

        return settings


class InvalidationRequest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    requested_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("Requested by"),
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
    )
    date_requested = models.DateTimeField(verbose_name=_("Date requested"))
    sites = models.ManyToManyField("wagtailcore.Site", verbose_name=_("Sites"))
    urls = models.TextField(verbose_name=_("Urls"))

    class Meta:
        ordering = ["-date_requested"]
        verbose_name = _("Invalidation request")
        verbose_name_plural = _("Invalidation requests")


@receiver(m2m_changed, sender=InvalidationRequest.sites.through)
def handle_invalidation_request(
    sender, instance: InvalidationRequest, action: str, **kwargs
):
    if action == "post_add":
        for site in instance.sites.all():
            urls = []
            root_url = site.root_url
            for path in instance.urls.splitlines():
                url = root_url + path
                urls.append(url)
            if ASYNC:
                signals.purge_urls_from_cache.send(
                    sender=sender, site_id=site.id, urls=urls
                )
            else:
                purge_urls_from_cache(site.id, urls)
