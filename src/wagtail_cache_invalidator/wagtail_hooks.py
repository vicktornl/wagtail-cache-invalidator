from django.contrib.auth.models import Permission
from django.urls import include, path, reverse
from django.utils.translation import gettext_lazy as _
from wagtail import hooks
from wagtail.admin.menu import Menu, MenuItem, SubmenuMenuItem
from wagtail.permission_policies import ModelPermissionPolicy
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup

from wagtail_cache_invalidator.models import InvalidationRequest


@hooks.register("register_admin_urls")
def register_admin_urls():
    return [
        path(
            "cache-invalidator/",
            include(
                "wagtail_cache_invalidator.admin_urls",
                namespace="wagtailcacheinvalidator",
            ),
        ),
    ]


@hooks.register("register_permissions")
def register_permissions():
    return Permission.objects.filter(
        content_type__app_label="wagtailcacheinvalidator",
        codename__in=["add_invalidationrequest"],
    )


class CacheMenuItem(MenuItem):
    def is_shown(self, request):
        return request.user.has_perm("wagtailcacheinvalidator.add_invalidationrequest")


class InvalidationRequestPermissionPolicy(ModelPermissionPolicy):
    def __init__(self):
        super().__init__(InvalidationRequest)

    def user_can_list(self, user):
        return user.has_perm("wagtailcacheinvalidator.add_invalidationrequest")

    def user_can_create(self, user):
        return False

    def user_can_edit_obj(self, user, obj):
        return False

    def user_can_delete_obj(self, user, obj):
        return True


class InvalidationRequestSnippetViewSet(SnippetViewSet):
    model = InvalidationRequest
    menu_label = _("Invalidation requests")
    icon = "list-ul"
    menu_order = 0
    list_display = ["requested_by", "date_requested", "display_sites", "urls"]
    list_filter = ["date_requested", "sites"]
    add_to_admin_menu = False
    permission_policy = InvalidationRequestPermissionPolicy()

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if qs is not None:
            qs = qs.select_related("requested_by")
            qs = qs.select_related("sites")
        return qs


class CacheSnippetViewSetGroup(SnippetViewSetGroup):
    menu_label = _("Cache")
    icon = "view"
    menu_order = 10000
    items = [InvalidationRequestSnippetViewSet]

    def get_submenu_items(self):
        items = super().get_submenu_items()
        items.append(
            CacheMenuItem(
                _("Purge"),
                reverse("wagtailcacheinvalidator:purge"),
                icon_name="bin",
                order=1,
            )
        )
        return items


register_snippet(CacheSnippetViewSetGroup)
