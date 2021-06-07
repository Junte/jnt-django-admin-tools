from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType

from jnt_admin_tools.mixins import (
    ClickableLinksAdminMixin,
    GenericForeignKeyAdminMixin,
    GenericForeignKeyInlineAdminMixin,
)
from jnt_admin_tools.mixins import AutocompleteAdminMixin
from jnt_admin_tools.mixins.base import BaseModelAdmin
from jnt_admin_tools.admin.content_type import BaseContentTypeAdmin
from test_app.filters import BarAutocompleteFilter, TagsAutocompleteFilter
from test_app.forms import GroupAdminForm
from test_app.models import Bar, Baz, Blog, Comment, Foo, Tag

admin.site.unregister(Group)


@admin.register(ContentType)
class ContentTypeAdmin(BaseContentTypeAdmin):
    """Register content type."""


class BazInlineAdmin(
    GenericForeignKeyInlineAdminMixin,
    AutocompleteAdminMixin,
    admin.TabularInline,
):
    model = Baz
    extra = 0
    fields = ("name", "foos", "owner")


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    form = GroupAdminForm
    readonly_fields = ("permissions",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("title",)
    fields = ("title",)
    search_fields = ("title",)


@admin.register(Foo)
class FooAdmin(BaseModelAdmin):
    list_display = ("name",)
    fields = ("name", "bar")
    search_fields = ("name",)
    list_filter = (BarAutocompleteFilter, "name")


@admin.register(Bar)
class BarAdmin(AutocompleteAdminMixin, admin.ModelAdmin):
    fields = ("name",)
    search_fields = ("name",)


@admin.register(Baz)
class BazAdmin(AutocompleteAdminMixin, admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(Blog)
class BlogAdmin(  # noqa: WPS215
    GenericForeignKeyAdminMixin,
    AutocompleteAdminMixin,
    ClickableLinksAdminMixin,
    admin.ModelAdmin,
):
    list_display = ("title", "author", "tags")
    readonly_fields = ("author", "tags")
    search_fields = ("title",)
    inlines = (BazInlineAdmin,)
    list_filter = (TagsAutocompleteFilter,)


@admin.register(Comment)
class CommentAdmin(
    GenericForeignKeyAdminMixin,
    AutocompleteAdminMixin,
    admin.ModelAdmin,
):
    fieldsets = (
        (None, {"fields": ("title", "content")}),
        (
            "Advanced options",
            {
                "fields": ("user", "link"),
            },
        ),
        (
            None,
            {
                "fields": ("owner",),
            },
        ),
    )
