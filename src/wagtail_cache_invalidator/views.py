from django.contrib import messages
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.utils import timezone
from django.utils.translation import gettext as _
from wagtail.admin.auth import permission_required
from wagtail.core.models import Site

from wagtail_cache_invalidator.forms import PurgeForm
from wagtail_cache_invalidator.models import InvalidationRequest


@permission_required("wagtailcacheinvalidator.add_invalidationrequest")
def purge(request):
    form = PurgeForm()

    if request.method == "POST":
        form = PurgeForm(request.POST)
        if form.is_valid():
            from wagtail_cache_invalidator.wagtail_hooks import (
                InvalidationRequestModelAdmin,
            )

            url_helper = InvalidationRequestModelAdmin().url_helper

            obj = InvalidationRequest(
                urls=form.cleaned_data.get("urls"),
                requested_by=request.user,
                date_requested=timezone.now(),
            )
            obj.save()
            obj.sites.set(form.cleaned_data.get("sites"))

            messages.add_message(
                request,
                messages.SUCCESS,
                _(
                    "Successfully added an invalidation request. Please wait a couple of seconds to ensure the cache is purged."
                ),
            )

            return HttpResponseRedirect(url_helper.get_action_url("index"))
    else:
        form = PurgeForm()

    context = {"form": form}

    return TemplateResponse(request, " wagtailcacheinvalidator/purge.html", context)
