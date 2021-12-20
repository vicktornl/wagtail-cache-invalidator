import uuid

from django.conf import settings
from django.db import models
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from wagtail.contrib.frontend_cache.utils import PurgeBatch


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
        batch = PurgeBatch()
        for site in instance.sites.all():
            for path in instance.urls.splitlines():
                url = site.root_url + path
                batch.add_url(url)
        batch.purge()
