"""Test models for E2E testing."""

from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.blocks import (
    CharBlock,
    ListBlock,
    RichTextBlock,
    StructBlock,
    TextBlock,
    URLBlock,
)
from wagtail.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Page
from wagtail.snippets.models import register_snippet


@register_snippet
class TestSnippet(models.Model):
    """Simple snippet model for testing."""

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ["name"]


class TestPage(Page):
    """Simple page model for testing page operations."""

    subtitle = models.CharField(max_length=255, blank=True)
    body = models.TextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("subtitle"),
        FieldPanel("body"),
    ]

    class Meta:
        verbose_name = "Test Page"


class StreamFieldPage(Page):
    """Page model with StreamField for testing StreamFieldHelper."""

    body = StreamField(
        [
            ("heading", CharBlock(form_classname="title")),
            ("paragraph", RichTextBlock()),
            ("quote", TextBlock()),
        ],
        use_json_field=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]

    class Meta:
        verbose_name = "StreamField Page"


# StructBlock for testing
class HeroBlock(StructBlock):
    """A hero section with title, subtitle, and optional image."""

    title = CharBlock(required=True)
    subtitle = CharBlock(required=False)
    image = ImageChooserBlock(required=False)

    class Meta:
        icon = "image"
        label = "Hero Section"


class LinkBlock(StructBlock):
    """A link with title and URL."""

    title = CharBlock(required=True)
    url = URLBlock(required=True)

    class Meta:
        icon = "link"
        label = "Link"


class AdvancedStreamFieldPage(Page):
    """Page model with advanced StreamField blocks for testing."""

    body = StreamField(
        [
            # Simple blocks
            ("heading", CharBlock(form_classname="title")),
            ("quote", TextBlock()),
            # StructBlock
            ("hero", HeroBlock()),
            # ListBlock with StructBlock
            ("links", ListBlock(LinkBlock())),
            # ListBlock with simple block
            ("items", ListBlock(CharBlock(label="Item"))),
            # ImageChooserBlock
            ("image", ImageChooserBlock()),
        ],
        use_json_field=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]

    class Meta:
        verbose_name = "Advanced StreamField Page"
