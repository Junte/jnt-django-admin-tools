from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType
from test_app.filters import BarAutocompleteFilter, TagsAutocompleteFilter
from test_app.forms import GroupAdminForm
from test_app.models import Bar, Baz, Blog, Comment, Foo, Tag

from jnt_admin_tools.admin.content_type import BaseContentTypeAdmin
from jnt_admin_tools.mixins import (
    AutocompleteAdminMixin,
    GenericForeignKeyAdminMixin,
    GenericForeignKeyInlineAdminMixin,
    ReadonlyWidgetsMixin,
)
from jnt_admin_tools.mixins.base import BaseModelAdmin

admin.site.unregister(Group)


@admin.register(ContentType)
class ContentTypeAdmin(BaseContentTypeAdmin):
    """Register content type."""


class BazInlineAdmin(  # noqa: WPS215
    ReadonlyWidgetsMixin,
    GenericForeignKeyInlineAdminMixin,
    AutocompleteAdminMixin,
    admin.TabularInline,
):
    model = Baz
    extra = 0
    fields = ("name", "foos", "owner")


@admin.register(Group)
class GroupAdmin(BaseModelAdmin):
    form = GroupAdminForm
    readonly_fields = ("permissions",)


@admin.register(Tag)
class TagAdmin(BaseModelAdmin, admin.ModelAdmin):
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
class BarAdmin(BaseModelAdmin):
    fields = ("name",)
    search_fields = ("name",)


@admin.register(Baz)
class BazAdmin(BaseModelAdmin):
    search_fields = ("name",)


@admin.register(Blog)
class BlogAdmin(  # noqa: WPS215
    GenericForeignKeyAdminMixin,
    BaseModelAdmin,
):
    list_display = ("title", "author", "tags")
    readonly_fields = ("author", "tags")
    search_fields = ("title",)
    inlines = (BazInlineAdmin,)
    list_filter = (TagsAutocompleteFilter,)


@admin.register(Comment)
class CommentAdmin(
    GenericForeignKeyAdminMixin,
    BaseModelAdmin,
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
