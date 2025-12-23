"""Test models for E2E testing."""

from django.db import models
from wagtail.admin.panels import FieldPanel
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
