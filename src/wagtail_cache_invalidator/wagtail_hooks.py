from django.contrib.auth.models import Permission
from django.urls import include, path, reverse
from django.utils.translation import gettext_lazy as _
from wagtail.admin.menu import Menu, MenuItem, SubmenuMenuItem
from wagtail.contrib.modeladmin.helpers.permission import PermissionHelper
from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    ModelAdminGroup,
    modeladmin_register,
)
from wagtail.core import hooks

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


class InvalidationRequestPermissionHelper(PermissionHelper):
    def user_can_create(self, user):
        return False

    def user_can_edit_obj(self, user, obj):
        return False

    def user_can_delete_obj(self, user, obj):
        return True


class InvalidationRequestModelAdmin(ModelAdmin):
    model = InvalidationRequest
    menu_label = _("Invalidation requests")
    menu_icon = "list-ul"
    menu_order = 0
    list_display = ["requested_by", "date_requested", "display_sites", "urls"]
    list_filter = ["date_requested", "sites"]
    permission_helper_class = InvalidationRequestPermissionHelper

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs.select_related("requested_by")
        qs.select_related("sites")
        return qs

    def display_sites(self, obj):
        return ", ".join([site.hostname for site in obj.sites.all()])

    display_sites.short_description = _("Sites")


class CacheModelAdminGroup(ModelAdminGroup):
    menu_label = _("Cache")
    menu_icon = "view"
    menu_order = 10000
    items = [InvalidationRequestModelAdmin]

    def get_submenu_items(self):
        items = super().get_submenu_items()
        items.append(
            CacheMenuItem(
                _("Purge"),
                reverse("wagtailcacheinvalidator:purge"),
                classnames="icon icon-bin",
                order=1,
            )
        )
        return items


modeladmin_register(CacheModelAdminGroup)
