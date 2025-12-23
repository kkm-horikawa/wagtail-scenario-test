"""Test models for E2E testing."""

from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.blocks import CharBlock, RichTextBlock, TextBlock
from wagtail.fields import StreamField
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
