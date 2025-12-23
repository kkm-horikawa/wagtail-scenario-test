"""E2E tests for StreamFieldHelper with Fluent Builder API."""

import pytest

from wagtail_scenario_test import PageAdminPage, StreamFieldHelper


@pytest.mark.e2e
@pytest.mark.django_db(transaction=True)
class TestStreamFieldHelperAddBlockE2E:
    """E2E tests for StreamFieldHelper.add_block()."""

    def test_add_heading_block(self, authenticated_page, server_url, home_page):
        """Test adding a heading block to StreamField."""
        page_admin = PageAdminPage(authenticated_page, server_url)

        # Navigate to add StreamFieldPage
        url = page_admin.add_child_page_url(home_page.id, "testapp", "streamfieldpage")
        page_admin.goto(url)
        page_admin.wait_for_navigation()

        # Create StreamFieldHelper
        sf = StreamFieldHelper(authenticated_page, "body")

        # Add heading block
        index = sf.add_block("Heading")

        # Verify block was added
        assert index == 0
        assert sf.get_block_count() == 1
        assert sf.get_block_type(0) == "heading"

    def test_add_multiple_blocks(self, authenticated_page, server_url, home_page):
        """Test adding multiple blocks to StreamField."""
        page_admin = PageAdminPage(authenticated_page, server_url)

        # Navigate to add StreamFieldPage
        url = page_admin.add_child_page_url(home_page.id, "testapp", "streamfieldpage")
        page_admin.goto(url)
        page_admin.wait_for_navigation()

        # Create StreamFieldHelper
        sf = StreamFieldHelper(authenticated_page, "body")

        # Add multiple blocks
        index1 = sf.add_block("Heading")
        index2 = sf.add_block("Quote")

        # Verify blocks were added
        assert index1 == 0
        assert index2 == 1
        assert sf.get_block_count() == 2
        assert sf.get_block_type(0) == "heading"
        assert sf.get_block_type(1) == "quote"

    def test_add_and_fill_block_fluent(self, authenticated_page, server_url, home_page):
        """Test adding a block and filling it using fluent API."""
        page_admin = PageAdminPage(authenticated_page, server_url)

        # Navigate to add StreamFieldPage
        url = page_admin.add_child_page_url(home_page.id, "testapp", "streamfieldpage")
        page_admin.goto(url)
        page_admin.wait_for_navigation()

        # Create StreamFieldHelper
        sf = StreamFieldHelper(authenticated_page, "body")

        # Add and fill heading block using fluent API
        index = sf.add_block("Heading")
        sf.block(index).fill("My Test Heading")

        # Verify value was filled
        input_field = authenticated_page.locator("#body-0-value")
        assert input_field.input_value() == "My Test Heading"

    def test_add_block_and_save_page(self, authenticated_page, server_url, home_page):
        """Test adding a block, filling it, and saving the page."""
        page_admin = PageAdminPage(authenticated_page, server_url)

        # Navigate to add StreamFieldPage
        url = page_admin.add_child_page_url(home_page.id, "testapp", "streamfieldpage")
        page_admin.goto(url)
        page_admin.wait_for_navigation()

        # Fill title
        authenticated_page.locator("#id_title").fill("StreamField Test Page")

        # Add and fill heading block using fluent API
        sf = StreamFieldHelper(authenticated_page, "body")
        index = sf.add_block("Heading")
        sf.block(index).fill("Welcome Heading")

        # Fill slug in Promote tab
        authenticated_page.get_by_role("tab", name="Promote").click()
        authenticated_page.locator("#id_slug").fill("streamfield-test-page")

        # Save as draft
        authenticated_page.get_by_role("button", name="Save draft").click()
        page_admin.wait_for_navigation()

        # Verify success
        page_admin.assert_success_message()

        # Verify page was created with StreamField content
        from tests.testapp.models import StreamFieldPage

        created_page = StreamFieldPage.objects.get(title="StreamField Test Page")
        assert len(created_page.body) == 1
        assert created_page.body[0].block_type == "heading"
        assert created_page.body[0].value == "Welcome Heading"


@pytest.mark.e2e
@pytest.mark.django_db(transaction=True)
class TestStreamFieldHelperStructBlockE2E:
    """E2E tests for StreamFieldHelper StructBlock methods with fluent API."""

    def test_add_and_fill_struct_block(self, authenticated_page, server_url, home_page):
        """Test adding a StructBlock and filling its fields with fluent API."""
        page_admin = PageAdminPage(authenticated_page, server_url)

        # Navigate to add AdvancedStreamFieldPage
        url = page_admin.add_child_page_url(
            home_page.id, "testapp", "advancedstreamfieldpage"
        )
        page_admin.goto(url)
        page_admin.wait_for_navigation()

        # Create StreamFieldHelper
        sf = StreamFieldHelper(authenticated_page, "body")

        # Add Hero Section block (StructBlock)
        index = sf.add_block("Hero Section")

        # Fill StructBlock fields using fluent API
        sf.block(index).struct("title").fill("Welcome to Our Site")
        sf.block(index).struct("subtitle").fill("The best place to be")

        # Verify values were filled using fluent API
        assert sf.block(index).struct("title").value() == "Welcome to Our Site"
        assert sf.block(index).struct("subtitle").value() == "The best place to be"

    def test_save_page_with_struct_block(
        self, authenticated_page, server_url, home_page
    ):
        """Test saving a page with StructBlock content."""
        page_admin = PageAdminPage(authenticated_page, server_url)

        # Navigate to add AdvancedStreamFieldPage
        url = page_admin.add_child_page_url(
            home_page.id, "testapp", "advancedstreamfieldpage"
        )
        page_admin.goto(url)
        page_admin.wait_for_navigation()

        # Fill title
        authenticated_page.locator("#id_title").fill("Advanced StreamField Test")

        # Add and fill Hero Section using fluent API
        sf = StreamFieldHelper(authenticated_page, "body")
        index = sf.add_block("Hero Section")
        sf.block(index).struct("title").fill("Hero Title")
        sf.block(index).struct("subtitle").fill("Hero Subtitle")

        # Fill slug
        authenticated_page.get_by_role("tab", name="Promote").click()
        authenticated_page.locator("#id_slug").fill("advanced-streamfield-test")

        # Save
        authenticated_page.get_by_role("button", name="Save draft").click()
        page_admin.wait_for_navigation()

        # Verify success
        page_admin.assert_success_message()

        # Verify content
        from tests.testapp.models import AdvancedStreamFieldPage

        created_page = AdvancedStreamFieldPage.objects.get(
            title="Advanced StreamField Test"
        )
        assert len(created_page.body) == 1
        assert created_page.body[0].block_type == "hero"
        assert created_page.body[0].value["title"] == "Hero Title"
        assert created_page.body[0].value["subtitle"] == "Hero Subtitle"


@pytest.mark.e2e
@pytest.mark.django_db(transaction=True)
class TestStreamFieldHelperListBlockE2E:
    """E2E tests for StreamFieldHelper ListBlock methods with fluent API."""

    def test_add_and_fill_list_block_with_struct(
        self, authenticated_page, server_url, home_page
    ):
        """Test adding a ListBlock with StructBlock items using fluent API."""
        page_admin = PageAdminPage(authenticated_page, server_url)

        # Navigate to add AdvancedStreamFieldPage
        url = page_admin.add_child_page_url(
            home_page.id, "testapp", "advancedstreamfieldpage"
        )
        page_admin.goto(url)
        page_admin.wait_for_navigation()

        # Fill title
        authenticated_page.locator("#id_title").fill("ListBlock Test Page")

        # Add Links block (ListBlock of LinkBlock StructBlock)
        sf = StreamFieldHelper(authenticated_page, "body")
        index = sf.add_block("Links")

        # ListBlock comes with one item by default, fill it using fluent API
        sf.block(index).item(0).struct("title").fill("Google")
        sf.block(index).item(0).struct("url").fill("https://google.com")

        # Verify values using fluent API
        assert sf.block(index).item(0).struct("title").value() == "Google"
        assert sf.block(index).item(0).struct("url").value() == "https://google.com"

        # Fill slug and save
        authenticated_page.get_by_role("tab", name="Promote").click()
        authenticated_page.locator("#id_slug").fill("listblock-test-page")
        authenticated_page.get_by_role("button", name="Save draft").click()
        page_admin.wait_for_navigation()

        # Verify success
        page_admin.assert_success_message()

        # Verify content
        from tests.testapp.models import AdvancedStreamFieldPage

        created_page = AdvancedStreamFieldPage.objects.get(title="ListBlock Test Page")
        assert len(created_page.body) == 1
        assert created_page.body[0].block_type == "links"
        assert len(created_page.body[0].value) == 1
        assert created_page.body[0].value[0]["title"] == "Google"
        assert created_page.body[0].value[0]["url"] == "https://google.com"

    def test_multiple_list_items(self, authenticated_page, server_url, home_page):
        """Test adding and filling multiple items in a ListBlock."""
        page_admin = PageAdminPage(authenticated_page, server_url)

        # Navigate to add AdvancedStreamFieldPage
        url = page_admin.add_child_page_url(
            home_page.id, "testapp", "advancedstreamfieldpage"
        )
        page_admin.goto(url)
        page_admin.wait_for_navigation()

        # Fill title
        authenticated_page.locator("#id_title").fill("Multiple Links Page")

        # Add Links block
        sf = StreamFieldHelper(authenticated_page, "body")
        index = sf.add_block("Links")

        # Fill first item (default)
        sf.block(index).item(0).struct("title").fill("Google")
        sf.block(index).item(0).struct("url").fill("https://google.com")

        # Add second item
        sf.block(index).add_item()
        sf.block(index).item(1).struct("title").fill("GitHub")
        sf.block(index).item(1).struct("url").fill("https://github.com")

        # Verify item count
        assert sf.block(index).item_count() == 2

        # Fill slug and save
        authenticated_page.get_by_role("tab", name="Promote").click()
        authenticated_page.locator("#id_slug").fill("multiple-links-page")
        authenticated_page.get_by_role("button", name="Save draft").click()
        page_admin.wait_for_navigation()

        # Verify success
        page_admin.assert_success_message()

        # Verify content
        from tests.testapp.models import AdvancedStreamFieldPage

        created_page = AdvancedStreamFieldPage.objects.get(title="Multiple Links Page")
        assert len(created_page.body[0].value) == 2
        assert created_page.body[0].value[0]["title"] == "Google"
        assert created_page.body[0].value[1]["title"] == "GitHub"


@pytest.mark.e2e
@pytest.mark.django_db(transaction=True)
class TestStreamFieldHelperMixedBlocksE2E:
    """E2E tests for mixed block types."""

    def test_multiple_block_types(self, authenticated_page, server_url, home_page):
        """Test page with multiple different block types."""
        page_admin = PageAdminPage(authenticated_page, server_url)

        # Navigate to add AdvancedStreamFieldPage
        url = page_admin.add_child_page_url(
            home_page.id, "testapp", "advancedstreamfieldpage"
        )
        page_admin.goto(url)
        page_admin.wait_for_navigation()

        # Fill title
        authenticated_page.locator("#id_title").fill("Mixed Blocks Page")

        sf = StreamFieldHelper(authenticated_page, "body")

        # Add heading block (simple)
        heading_idx = sf.add_block("Heading")
        sf.block(heading_idx).fill("Page Title")

        # Add Hero Section (StructBlock)
        hero_idx = sf.add_block("Hero Section")
        sf.block(hero_idx).struct("title").fill("Hero Title")
        sf.block(hero_idx).struct("subtitle").fill("Hero Subtitle")

        # Add Links (ListBlock)
        links_idx = sf.add_block("Links")
        sf.block(links_idx).item(0).struct("title").fill("First Link")
        sf.block(links_idx).item(0).struct("url").fill("https://example.com")

        # Verify block count
        assert sf.get_block_count() == 3

        # Verify block types
        assert sf.get_block_type(heading_idx) == "heading"
        assert sf.get_block_type(hero_idx) == "hero"
        assert sf.get_block_type(links_idx) == "links"

        # Fill slug and save
        authenticated_page.get_by_role("tab", name="Promote").click()
        authenticated_page.locator("#id_slug").fill("mixed-blocks-page")
        authenticated_page.get_by_role("button", name="Save draft").click()
        page_admin.wait_for_navigation()

        # Verify success
        page_admin.assert_success_message()

        # Verify content
        from tests.testapp.models import AdvancedStreamFieldPage

        created_page = AdvancedStreamFieldPage.objects.get(title="Mixed Blocks Page")
        assert len(created_page.body) == 3
        assert created_page.body[0].block_type == "heading"
        assert created_page.body[0].value == "Page Title"
        assert created_page.body[1].block_type == "hero"
        assert created_page.body[1].value["title"] == "Hero Title"
        assert created_page.body[2].block_type == "links"
        assert created_page.body[2].value[0]["title"] == "First Link"
