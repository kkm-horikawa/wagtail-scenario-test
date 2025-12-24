"""Test models for E2E testing."""

from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.blocks import (
    BlockQuoteBlock,
    BooleanBlock,
    CharBlock,
    ChoiceBlock,
    DateBlock,
    DateTimeBlock,
    DecimalBlock,
    EmailBlock,
    FloatBlock,
    IntegerBlock,
    ListBlock,
    MultipleChoiceBlock,
    PageChooserBlock,
    RawHTMLBlock,
    RegexBlock,
    RichTextBlock,
    StreamBlock,
    StructBlock,
    TextBlock,
    TimeBlock,
    URLBlock,
)
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Page
from wagtail.snippets.blocks import SnippetChooserBlock
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


class CardBlock(StructBlock):
    """A card with title and description."""

    title = CharBlock(required=True)
    description = TextBlock(required=False)

    class Meta:
        icon = "doc-full"
        label = "Card"


class SectionBlock(StructBlock):
    """A section with heading and cards (for deep nesting tests)."""

    heading = CharBlock(required=True)
    cards = ListBlock(CardBlock())

    class Meta:
        icon = "folder-open-inverse"
        label = "Section"


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
            # SnippetChooserBlock
            ("snippet", SnippetChooserBlock("testapp.TestSnippet")),
            # PageChooserBlock
            ("related_page", PageChooserBlock()),
            # DocumentChooserBlock
            ("document", DocumentChooserBlock()),
            # Deep nesting: StructBlock > ListBlock > StructBlock
            ("section", SectionBlock()),
        ],
        use_json_field=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]

    class Meta:
        verbose_name = "Advanced StreamField Page"


# Nested StreamBlock for testing
class NestedContentBlock(StreamBlock):
    """A nested StreamBlock for testing StreamBlock within StreamField."""

    text = CharBlock()
    quote = BlockQuoteBlock()


class AllBlockTypesPage(Page):
    """Page model with ALL StreamField block types for comprehensive testing."""

    body = StreamField(
        [
            # ===== Text Input Blocks =====
            ("char", CharBlock(label="Char Block")),
            ("text", TextBlock(label="Text Block")),
            ("email", EmailBlock(label="Email Block")),
            ("url", URLBlock(label="URL Block")),
            (
                "regex",
                RegexBlock(regex=r"^[A-Z]{3}$", label="Regex Block (3 uppercase)"),
            ),
            # ===== Numeric Blocks =====
            ("integer", IntegerBlock(label="Integer Block")),
            ("float", FloatBlock(label="Float Block")),
            ("decimal", DecimalBlock(label="Decimal Block", decimal_places=2)),
            # ===== Date/Time Blocks =====
            ("date", DateBlock(label="Date Block")),
            ("time", TimeBlock(label="Time Block")),
            ("datetime", DateTimeBlock(label="DateTime Block")),
            # ===== Content Blocks =====
            ("richtext", RichTextBlock(label="Rich Text Block")),
            ("rawhtml", RawHTMLBlock(label="Raw HTML Block")),
            ("blockquote", BlockQuoteBlock(label="Block Quote")),
            # ===== Selection Blocks =====
            (
                "boolean",
                BooleanBlock(label="Boolean Block", required=False),
            ),
            (
                "choice",
                ChoiceBlock(
                    choices=[
                        ("option1", "Option 1"),
                        ("option2", "Option 2"),
                        ("option3", "Option 3"),
                    ],
                    label="Choice Block",
                ),
            ),
            (
                "multiple_choice",
                MultipleChoiceBlock(
                    choices=[
                        ("red", "Red"),
                        ("green", "Green"),
                        ("blue", "Blue"),
                    ],
                    label="Multiple Choice Block",
                ),
            ),
            # ===== Chooser Blocks =====
            ("image", ImageChooserBlock(label="Image Block")),
            ("document", DocumentChooserBlock(label="Document Block")),
            ("page", PageChooserBlock(label="Page Block")),
            (
                "snippet",
                SnippetChooserBlock("testapp.TestSnippet", label="Snippet Block"),
            ),
            ("embed", EmbedBlock(label="Embed Block")),
            # ===== Structural Blocks =====
            ("struct", HeroBlock()),
            ("list", ListBlock(CharBlock(label="Item"), label="List Block")),
            ("nested_stream", NestedContentBlock(label="Nested Stream Block")),
        ],
        use_json_field=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]

    class Meta:
        verbose_name = "All Block Types Page"
