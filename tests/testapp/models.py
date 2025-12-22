"""Test models for E2E testing."""

from django.db import models
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
