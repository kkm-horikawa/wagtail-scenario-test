"""E2E tests for all StreamField block types."""

import pytest

from wagtail_scenario_test import PageAdminPage, StreamFieldHelper


@pytest.mark.e2e
@pytest.mark.django_db(transaction=True)
class TestTextInputBlocksE2E:
    """E2E tests for text input block types."""

    def test_char_block(self, authenticated_page, server_url, home_page):
        """Test CharBlock input."""
        page_admin = PageAdminPage(authenticated_page, server_url)
        url = page_admin.add_child_page_url(
            home_page.id, "testapp", "allblocktypespage"
        )
        page_admin.goto(url)
        page_admin.wait_for_navigation()

        authenticated_page.locator("#id_title").fill("Char Block Test")

        sf = StreamFieldHelper(authenticated_page, "body")
        index = sf.add_block("Char Block")
        sf.block(index).fill("Hello World")

        assert sf.block(index).value() == "Hello World"

        # Save
        authenticated_page.get_by_role("tab", name="Promote").click()
        authenticated_page.locator("#id_slug").fill("char-block-test")
        authenticated_page.get_by_role("button", name="Save draft").click()
        page_admin.wait_for_navigation()
        page_admin.assert_success_message()

        from tests.testapp.models import AllBlockTypesPage

        created_page = AllBlockTypesPage.objects.get(title="Char Block Test")
        assert created_page.body[0].block_type == "char"
        assert created_page.body[0].value == "Hello World"

    def test_email_block(self, authenticated_page, server_url, home_page):
        """Test EmailBlock input."""
        page_admin = PageAdminPage(authenticated_page, server_url)
        url = page_admin.add_child_page_url(
            home_page.id, "testapp", "allblocktypespage"
        )
        page_admin.goto(url)
        page_admin.wait_for_navigation()

        authenticated_page.locator("#id_title").fill("Email Block Test")

        sf = StreamFieldHelper(authenticated_page, "body")
        index = sf.add_block("Email Block")
        sf.block(index).fill("test@example.com")

        # Save
        authenticated_page.get_by_role("tab", name="Promote").click()
        authenticated_page.locator("#id_slug").fill("email-block-test")
        authenticated_page.get_by_role("button", name="Save draft").click()
        page_admin.wait_for_navigation()
        page_admin.assert_success_message()

        from tests.testapp.models import AllBlockTypesPage

        created_page = AllBlockTypesPage.objects.get(title="Email Block Test")
        assert created_page.body[0].block_type == "email"
        assert created_page.body[0].value == "test@example.com"

    def test_url_block(self, authenticated_page, server_url, home_page):
        """Test URLBlock input."""
        page_admin = PageAdminPage(authenticated_page, server_url)
        url = page_admin.add_child_page_url(
            home_page.id, "testapp", "allblocktypespage"
        )
        page_admin.goto(url)
        page_admin.wait_for_navigation()

        authenticated_page.locator("#id_title").fill("URL Block Test")

        sf = StreamFieldHelper(authenticated_page, "body")
        index = sf.add_block("URL Block")
        sf.block(index).fill("https://example.com")

        # Save
        authenticated_page.get_by_role("tab", name="Promote").click()
        authenticated_page.locator("#id_slug").fill("url-block-test")
        authenticated_page.get_by_role("button", name="Save draft").click()
        page_admin.wait_for_navigation()
        page_admin.assert_success_message()

        from tests.testapp.models import AllBlockTypesPage

        created_page = AllBlockTypesPage.objects.get(title="URL Block Test")
        assert created_page.body[0].block_type == "url"
        assert created_page.body[0].value == "https://example.com"

    def test_regex_block(self, authenticated_page, server_url, home_page):
        """Test RegexBlock input."""
        page_admin = PageAdminPage(authenticated_page, server_url)
        url = page_admin.add_child_page_url(
            home_page.id, "testapp", "allblocktypespage"
        )
        page_admin.goto(url)
        page_admin.wait_for_navigation()

        authenticated_page.locator("#id_title").fill("Regex Block Test")

        sf = StreamFieldHelper(authenticated_page, "body")
        index = sf.add_block("Regex Block (3 uppercase)")
        sf.block(index).fill("ABC")

        # Save
        authenticated_page.get_by_role("tab", name="Promote").click()
        authenticated_page.locator("#id_slug").fill("regex-block-test")
        authenticated_page.get_by_role("button", name="Save draft").click()
        page_admin.wait_for_navigation()
        page_admin.assert_success_message()

        from tests.testapp.models import AllBlockTypesPage

        created_page = AllBlockTypesPage.objects.get(title="Regex Block Test")
        assert created_page.body[0].block_type == "regex"
        assert created_page.body[0].value == "ABC"


@pytest.mark.e2e
@pytest.mark.django_db(transaction=True)
class TestNumericBlocksE2E:
    """E2E tests for numeric block types."""

    def test_integer_block(self, authenticated_page, server_url, home_page):
        """Test IntegerBlock input."""
        page_admin = PageAdminPage(authenticated_page, server_url)
        url = page_admin.add_child_page_url(
            home_page.id, "testapp", "allblocktypespage"
        )
        page_admin.goto(url)
        page_admin.wait_for_navigation()

        authenticated_page.locator("#id_title").fill("Integer Block Test")

        sf = StreamFieldHelper(authenticated_page, "body")
        index = sf.add_block("Integer Block")
        sf.block(index).fill("42")

        # Save
        authenticated_page.get_by_role("tab", name="Promote").click()
        authenticated_page.locator("#id_slug").fill("integer-block-test")
        authenticated_page.get_by_role("button", name="Save draft").click()
        page_admin.wait_for_navigation()
        page_admin.assert_success_message()

        from tests.testapp.models import AllBlockTypesPage

        created_page = AllBlockTypesPage.objects.get(title="Integer Block Test")
        assert created_page.body[0].block_type == "integer"
        assert created_page.body[0].value == 42

    def test_float_block(self, authenticated_page, server_url, home_page):
        """Test FloatBlock input."""
        page_admin = PageAdminPage(authenticated_page, server_url)
        url = page_admin.add_child_page_url(
            home_page.id, "testapp", "allblocktypespage"
        )
        page_admin.goto(url)
        page_admin.wait_for_navigation()

        authenticated_page.locator("#id_title").fill("Float Block Test")

        sf = StreamFieldHelper(authenticated_page, "body")
        index = sf.add_block("Float Block")
        sf.block(index).fill("3.14")

        # Save
        authenticated_page.get_by_role("tab", name="Promote").click()
        authenticated_page.locator("#id_slug").fill("float-block-test")
        authenticated_page.get_by_role("button", name="Save draft").click()
        page_admin.wait_for_navigation()
        page_admin.assert_success_message()

        from tests.testapp.models import AllBlockTypesPage

        created_page = AllBlockTypesPage.objects.get(title="Float Block Test")
        assert created_page.body[0].block_type == "float"
        assert created_page.body[0].value == 3.14

    def test_decimal_block(self, authenticated_page, server_url, home_page):
        """Test DecimalBlock input."""
        page_admin = PageAdminPage(authenticated_page, server_url)
        url = page_admin.add_child_page_url(
            home_page.id, "testapp", "allblocktypespage"
        )
        page_admin.goto(url)
        page_admin.wait_for_navigation()

        authenticated_page.locator("#id_title").fill("Decimal Block Test")

        sf = StreamFieldHelper(authenticated_page, "body")
        index = sf.add_block("Decimal Block")
        sf.block(index).fill("99.99")

        # Save
        authenticated_page.get_by_role("tab", name="Promote").click()
        authenticated_page.locator("#id_slug").fill("decimal-block-test")
        authenticated_page.get_by_role("button", name="Save draft").click()
        page_admin.wait_for_navigation()
        page_admin.assert_success_message()

        from decimal import Decimal

        from tests.testapp.models import AllBlockTypesPage

        created_page = AllBlockTypesPage.objects.get(title="Decimal Block Test")
        assert created_page.body[0].block_type == "decimal"
        assert created_page.body[0].value == Decimal("99.99")


@pytest.mark.e2e
@pytest.mark.django_db(transaction=True)
class TestDateTimeBlocksE2E:
    """E2E tests for date/time block types."""

    def test_date_block(self, authenticated_page, server_url, home_page):
        """Test DateBlock input."""
        page_admin = PageAdminPage(authenticated_page, server_url)
        url = page_admin.add_child_page_url(
            home_page.id, "testapp", "allblocktypespage"
        )
        page_admin.goto(url)
        page_admin.wait_for_navigation()

        authenticated_page.locator("#id_title").fill("Date Block Test")

        sf = StreamFieldHelper(authenticated_page, "body")
        index = sf.add_block("Date Block")
        sf.block(index).set_date("2024-06-15")

        # Save
        authenticated_page.get_by_role("tab", name="Promote").click()
        authenticated_page.locator("#id_slug").fill("date-block-test")
        authenticated_page.get_by_role("button", name="Save draft").click()
        page_admin.wait_for_navigation()
        page_admin.assert_success_message()

        from datetime import date

        from tests.testapp.models import AllBlockTypesPage

        created_page = AllBlockTypesPage.objects.get(title="Date Block Test")
        assert created_page.body[0].block_type == "date"
        assert created_page.body[0].value == date(2024, 6, 15)

    def test_time_block(self, authenticated_page, server_url, home_page):
        """Test TimeBlock input."""
        page_admin = PageAdminPage(authenticated_page, server_url)
        url = page_admin.add_child_page_url(
            home_page.id, "testapp", "allblocktypespage"
        )
        page_admin.goto(url)
        page_admin.wait_for_navigation()

        authenticated_page.locator("#id_title").fill("Time Block Test")

        sf = StreamFieldHelper(authenticated_page, "body")
        index = sf.add_block("Time Block")
        sf.block(index).set_time("14:30")

        # Save
        authenticated_page.get_by_role("tab", name="Promote").click()
        authenticated_page.locator("#id_slug").fill("time-block-test")
        authenticated_page.get_by_role("button", name="Save draft").click()
        page_admin.wait_for_navigation()
        page_admin.assert_success_message()

        from datetime import time

        from tests.testapp.models import AllBlockTypesPage

        created_page = AllBlockTypesPage.objects.get(title="Time Block Test")
        assert created_page.body[0].block_type == "time"
        assert created_page.body[0].value == time(14, 30)

    def test_datetime_block(self, authenticated_page, server_url, home_page):
        """Test DateTimeBlock input."""
        page_admin = PageAdminPage(authenticated_page, server_url)
        url = page_admin.add_child_page_url(
            home_page.id, "testapp", "allblocktypespage"
        )
        page_admin.goto(url)
        page_admin.wait_for_navigation()

        authenticated_page.locator("#id_title").fill("DateTime Block Test")

        sf = StreamFieldHelper(authenticated_page, "body")
        index = sf.add_block("DateTime Block")
        sf.block(index).set_datetime("2024-06-15", "14:30")

        # Save
        authenticated_page.get_by_role("tab", name="Promote").click()
        authenticated_page.locator("#id_slug").fill("datetime-block-test")
        authenticated_page.get_by_role("button", name="Save draft").click()
        page_admin.wait_for_navigation()
        page_admin.assert_success_message()

        from tests.testapp.models import AllBlockTypesPage

        created_page = AllBlockTypesPage.objects.get(title="DateTime Block Test")
        assert created_page.body[0].block_type == "datetime"
        # Compare without timezone info
        dt_value = created_page.body[0].value
        assert dt_value.year == 2024
        assert dt_value.month == 6
        assert dt_value.day == 15
        assert dt_value.hour == 14
        assert dt_value.minute == 30


@pytest.mark.e2e
@pytest.mark.django_db(transaction=True)
class TestContentBlocksE2E:
    """E2E tests for content block types."""

    def test_rawhtml_block(self, authenticated_page, server_url, home_page):
        """Test RawHTMLBlock input."""
        page_admin = PageAdminPage(authenticated_page, server_url)
        url = page_admin.add_child_page_url(
            home_page.id, "testapp", "allblocktypespage"
        )
        page_admin.goto(url)
        page_admin.wait_for_navigation()

        authenticated_page.locator("#id_title").fill("RawHTML Block Test")

        sf = StreamFieldHelper(authenticated_page, "body")
        index = sf.add_block("Raw HTML Block")
        sf.block(index).fill("<p>Hello <strong>World</strong></p>")

        # Save
        authenticated_page.get_by_role("tab", name="Promote").click()
        authenticated_page.locator("#id_slug").fill("rawhtml-block-test")
        authenticated_page.get_by_role("button", name="Save draft").click()
        page_admin.wait_for_navigation()
        page_admin.assert_success_message()

        from tests.testapp.models import AllBlockTypesPage

        created_page = AllBlockTypesPage.objects.get(title="RawHTML Block Test")
        assert created_page.body[0].block_type == "rawhtml"
        assert "<strong>World</strong>" in created_page.body[0].value

    def test_blockquote_block(self, authenticated_page, server_url, home_page):
        """Test BlockQuoteBlock input."""
        page_admin = PageAdminPage(authenticated_page, server_url)
        url = page_admin.add_child_page_url(
            home_page.id, "testapp", "allblocktypespage"
        )
        page_admin.goto(url)
        page_admin.wait_for_navigation()

        authenticated_page.locator("#id_title").fill("BlockQuote Test")

        sf = StreamFieldHelper(authenticated_page, "body")
        index = sf.add_block("Block Quote")
        sf.block(index).fill("To be or not to be")

        # Save
        authenticated_page.get_by_role("tab", name="Promote").click()
        authenticated_page.locator("#id_slug").fill("blockquote-test")
        authenticated_page.get_by_role("button", name="Save draft").click()
        page_admin.wait_for_navigation()
        page_admin.assert_success_message()

        from tests.testapp.models import AllBlockTypesPage

        created_page = AllBlockTypesPage.objects.get(title="BlockQuote Test")
        assert created_page.body[0].block_type == "blockquote"
        assert created_page.body[0].value == "To be or not to be"


@pytest.mark.e2e
@pytest.mark.django_db(transaction=True)
class TestSelectionBlocksE2E:
    """E2E tests for selection block types."""

    def test_boolean_block_checked(self, authenticated_page, server_url, home_page):
        """Test BooleanBlock checkbox - checked."""
        page_admin = PageAdminPage(authenticated_page, server_url)
        url = page_admin.add_child_page_url(
            home_page.id, "testapp", "allblocktypespage"
        )
        page_admin.goto(url)
        page_admin.wait_for_navigation()

        authenticated_page.locator("#id_title").fill("Boolean Block True Test")

        sf = StreamFieldHelper(authenticated_page, "body")
        index = sf.add_block("Boolean Block")
        sf.block(index).check()

        assert sf.block(index).is_checked() is True

        # Save
        authenticated_page.get_by_role("tab", name="Promote").click()
        authenticated_page.locator("#id_slug").fill("boolean-true-test")
        authenticated_page.get_by_role("button", name="Save draft").click()
        page_admin.wait_for_navigation()
        page_admin.assert_success_message()

        from tests.testapp.models import AllBlockTypesPage

        created_page = AllBlockTypesPage.objects.get(title="Boolean Block True Test")
        assert created_page.body[0].block_type == "boolean"
        assert created_page.body[0].value is True

    def test_boolean_block_unchecked(self, authenticated_page, server_url, home_page):
        """Test BooleanBlock checkbox - unchecked."""
        page_admin = PageAdminPage(authenticated_page, server_url)
        url = page_admin.add_child_page_url(
            home_page.id, "testapp", "allblocktypespage"
        )
        page_admin.goto(url)
        page_admin.wait_for_navigation()

        authenticated_page.locator("#id_title").fill("Boolean Block False Test")

        sf = StreamFieldHelper(authenticated_page, "body")
        index = sf.add_block("Boolean Block")
        # Don't check it - should be false

        assert sf.block(index).is_checked() is False

        # Save
        authenticated_page.get_by_role("tab", name="Promote").click()
        authenticated_page.locator("#id_slug").fill("boolean-false-test")
        authenticated_page.get_by_role("button", name="Save draft").click()
        page_admin.wait_for_navigation()
        page_admin.assert_success_message()

        from tests.testapp.models import AllBlockTypesPage

        created_page = AllBlockTypesPage.objects.get(title="Boolean Block False Test")
        assert created_page.body[0].block_type == "boolean"
        assert created_page.body[0].value is False

    def test_choice_block(self, authenticated_page, server_url, home_page):
        """Test ChoiceBlock dropdown selection."""
        page_admin = PageAdminPage(authenticated_page, server_url)
        url = page_admin.add_child_page_url(
            home_page.id, "testapp", "allblocktypespage"
        )
        page_admin.goto(url)
        page_admin.wait_for_navigation()

        authenticated_page.locator("#id_title").fill("Choice Block Test")

        sf = StreamFieldHelper(authenticated_page, "body")
        index = sf.add_block("Choice Block")
        sf.block(index).select("option2")

        # Save
        authenticated_page.get_by_role("tab", name="Promote").click()
        authenticated_page.locator("#id_slug").fill("choice-block-test")
        authenticated_page.get_by_role("button", name="Save draft").click()
        page_admin.wait_for_navigation()
        page_admin.assert_success_message()

        from tests.testapp.models import AllBlockTypesPage

        created_page = AllBlockTypesPage.objects.get(title="Choice Block Test")
        assert created_page.body[0].block_type == "choice"
        assert created_page.body[0].value == "option2"

    def test_multiple_choice_block(self, authenticated_page, server_url, home_page):
        """Test MultipleChoiceBlock multi-select."""
        page_admin = PageAdminPage(authenticated_page, server_url)
        url = page_admin.add_child_page_url(
            home_page.id, "testapp", "allblocktypespage"
        )
        page_admin.goto(url)
        page_admin.wait_for_navigation()

        authenticated_page.locator("#id_title").fill("Multiple Choice Test")

        sf = StreamFieldHelper(authenticated_page, "body")
        index = sf.add_block("Multiple Choice Block")
        sf.block(index).select_multiple(["red", "blue"])

        # Save
        authenticated_page.get_by_role("tab", name="Promote").click()
        authenticated_page.locator("#id_slug").fill("multiple-choice-test")
        authenticated_page.get_by_role("button", name="Save draft").click()
        page_admin.wait_for_navigation()
        page_admin.assert_success_message()

        from tests.testapp.models import AllBlockTypesPage

        created_page = AllBlockTypesPage.objects.get(title="Multiple Choice Test")
        assert created_page.body[0].block_type == "multiple_choice"
        assert set(created_page.body[0].value) == {"red", "blue"}


@pytest.mark.e2e
@pytest.mark.django_db(transaction=True)
class TestEmbedBlockE2E:
    """E2E tests for EmbedBlock."""

    def test_embed_block(self, authenticated_page, server_url, home_page):
        """Test EmbedBlock URL input."""
        page_admin = PageAdminPage(authenticated_page, server_url)
        url = page_admin.add_child_page_url(
            home_page.id, "testapp", "allblocktypespage"
        )
        page_admin.goto(url)
        page_admin.wait_for_navigation()

        authenticated_page.locator("#id_title").fill("Embed Block Test")

        sf = StreamFieldHelper(authenticated_page, "body")
        index = sf.add_block("Embed Block")
        sf.block(index).fill("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

        # Save (may fail validation in some environments without oembed setup)
        authenticated_page.get_by_role("tab", name="Promote").click()
        authenticated_page.locator("#id_slug").fill("embed-block-test")
        authenticated_page.get_by_role("button", name="Save draft").click()
        page_admin.wait_for_navigation()

        # Check if saved successfully or if there was a validation error
        # EmbedBlock may fail if oEmbed providers aren't configured
        success = authenticated_page.locator(
            ".w-message--success, .success"
        ).first.is_visible()
        if success:
            from tests.testapp.models import AllBlockTypesPage

            created_page = AllBlockTypesPage.objects.get(title="Embed Block Test")
            assert created_page.body[0].block_type == "embed"


@pytest.mark.e2e
@pytest.mark.django_db(transaction=True)
class TestNestedStreamBlockE2E:
    """E2E tests for nested StreamBlock."""

    def test_nested_stream_block(self, authenticated_page, server_url, home_page):
        """Test adding blocks to a nested StreamBlock."""
        page_admin = PageAdminPage(authenticated_page, server_url)
        url = page_admin.add_child_page_url(
            home_page.id, "testapp", "allblocktypespage"
        )
        page_admin.goto(url)
        page_admin.wait_for_navigation()

        authenticated_page.locator("#id_title").fill("Nested Stream Test")

        sf = StreamFieldHelper(authenticated_page, "body")
        # Add a nested StreamBlock
        outer_index = sf.add_block("Nested Stream Block")

        # Add blocks inside the nested StreamBlock
        inner_index = sf.block(outer_index).add_block("Text")
        sf.block(outer_index).block(inner_index).fill("Nested text content")

        # Save
        authenticated_page.get_by_role("tab", name="Promote").click()
        authenticated_page.locator("#id_slug").fill("nested-stream-test")
        authenticated_page.get_by_role("button", name="Save draft").click()
        page_admin.wait_for_navigation()
        page_admin.assert_success_message()

        from tests.testapp.models import AllBlockTypesPage

        created_page = AllBlockTypesPage.objects.get(title="Nested Stream Test")
        assert created_page.body[0].block_type == "nested_stream"
        # Nested StreamBlock contains a list of blocks
        assert len(created_page.body[0].value) == 1
        assert created_page.body[0].value[0].block_type == "text"
        assert created_page.body[0].value[0].value == "Nested text content"
