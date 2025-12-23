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


@pytest.mark.e2e
@pytest.mark.django_db(transaction=True)
class TestStreamFieldHelperSimpleListBlockE2E:
    """E2E tests for simple ListBlock (CharBlock items)."""

    def test_simple_list_block_single_item(
        self, authenticated_page, server_url, home_page
    ):
        """Test ListBlock with simple CharBlock items."""
        page_admin = PageAdminPage(authenticated_page, server_url)

        url = page_admin.add_child_page_url(
            home_page.id, "testapp", "advancedstreamfieldpage"
        )
        page_admin.goto(url)
        page_admin.wait_for_navigation()

        authenticated_page.locator("#id_title").fill("Simple List Page")

        sf = StreamFieldHelper(authenticated_page, "body")

        # Add Items block (ListBlock of CharBlock)
        index = sf.add_block("Items")

        # Fill the first item (default)
        sf.block(index).item(0).fill("First Item")

        # Verify value
        assert sf.block(index).item(0).value() == "First Item"

        # Save
        authenticated_page.get_by_role("tab", name="Promote").click()
        authenticated_page.locator("#id_slug").fill("simple-list-page")
        authenticated_page.get_by_role("button", name="Save draft").click()
        page_admin.wait_for_navigation()

        page_admin.assert_success_message()

        from tests.testapp.models import AdvancedStreamFieldPage

        created_page = AdvancedStreamFieldPage.objects.get(title="Simple List Page")
        assert created_page.body[0].block_type == "items"
        assert created_page.body[0].value[0] == "First Item"

    def test_simple_list_block_multiple_items(
        self, authenticated_page, server_url, home_page
    ):
        """Test adding multiple items to a simple ListBlock."""
        page_admin = PageAdminPage(authenticated_page, server_url)

        url = page_admin.add_child_page_url(
            home_page.id, "testapp", "advancedstreamfieldpage"
        )
        page_admin.goto(url)
        page_admin.wait_for_navigation()

        authenticated_page.locator("#id_title").fill("Multi Item List Page")

        sf = StreamFieldHelper(authenticated_page, "body")
        index = sf.add_block("Items")

        # Fill first item
        sf.block(index).item(0).fill("Apple")

        # Add and fill more items
        sf.block(index).add_item()
        sf.block(index).item(1).fill("Banana")

        sf.block(index).add_item()
        sf.block(index).item(2).fill("Cherry")

        # Verify item count
        assert sf.block(index).item_count() == 3

        # Verify values
        assert sf.block(index).item(0).value() == "Apple"
        assert sf.block(index).item(1).value() == "Banana"
        assert sf.block(index).item(2).value() == "Cherry"

        # Save
        authenticated_page.get_by_role("tab", name="Promote").click()
        authenticated_page.locator("#id_slug").fill("multi-item-list-page")
        authenticated_page.get_by_role("button", name="Save draft").click()
        page_admin.wait_for_navigation()

        page_admin.assert_success_message()

        from tests.testapp.models import AdvancedStreamFieldPage

        created_page = AdvancedStreamFieldPage.objects.get(title="Multi Item List Page")
        assert len(created_page.body[0].value) == 3
        assert created_page.body[0].value[0] == "Apple"
        assert created_page.body[0].value[1] == "Banana"
        assert created_page.body[0].value[2] == "Cherry"


@pytest.mark.e2e
@pytest.mark.django_db(transaction=True)
class TestStreamFieldHelperTextBlockE2E:
    """E2E tests for TextBlock (textarea)."""

    def test_text_block_fill_and_save(self, authenticated_page, server_url, home_page):
        """Test filling a TextBlock (quote) with multiline content."""
        page_admin = PageAdminPage(authenticated_page, server_url)

        url = page_admin.add_child_page_url(
            home_page.id, "testapp", "advancedstreamfieldpage"
        )
        page_admin.goto(url)
        page_admin.wait_for_navigation()

        authenticated_page.locator("#id_title").fill("Quote Page")

        sf = StreamFieldHelper(authenticated_page, "body")

        # Add Quote block (TextBlock)
        index = sf.add_block("Quote")

        # Fill with multiline text
        quote_text = "To be or not to be,\nthat is the question."
        sf.block(index).fill(quote_text)

        # Save
        authenticated_page.get_by_role("tab", name="Promote").click()
        authenticated_page.locator("#id_slug").fill("quote-page")
        authenticated_page.get_by_role("button", name="Save draft").click()
        page_admin.wait_for_navigation()

        page_admin.assert_success_message()

        from tests.testapp.models import AdvancedStreamFieldPage

        created_page = AdvancedStreamFieldPage.objects.get(title="Quote Page")
        assert created_page.body[0].block_type == "quote"
        assert "To be or not to be" in created_page.body[0].value


@pytest.mark.e2e
@pytest.mark.django_db(transaction=True)
class TestStreamFieldHelperDeepNestingE2E:
    """E2E tests for deeply nested block structures."""

    def test_struct_with_list_of_structs(
        self, authenticated_page, server_url, home_page
    ):
        """Test StructBlock > ListBlock > StructBlock nesting."""
        page_admin = PageAdminPage(authenticated_page, server_url)

        url = page_admin.add_child_page_url(
            home_page.id, "testapp", "advancedstreamfieldpage"
        )
        page_admin.goto(url)
        page_admin.wait_for_navigation()

        authenticated_page.locator("#id_title").fill("Deep Nesting Page")

        sf = StreamFieldHelper(authenticated_page, "body")

        # Add Section block (StructBlock with heading and ListBlock of CardBlocks)
        index = sf.add_block("Section")

        # Fill section heading
        sf.block(index).struct("heading").fill("Featured Cards")

        # Fill first card (default item in ListBlock)
        sf.block(index).struct("cards").item(0).struct("title").fill("Card 1")
        sf.block(index).struct("cards").item(0).struct("description").fill(
            "First card description"
        )

        # Verify values at deep nesting level
        assert sf.block(index).struct("heading").value() == "Featured Cards"
        assert sf.block(index).struct("cards").item(0).struct("title").value() == (
            "Card 1"
        )

        # Save
        authenticated_page.get_by_role("tab", name="Promote").click()
        authenticated_page.locator("#id_slug").fill("deep-nesting-page")
        authenticated_page.get_by_role("button", name="Save draft").click()
        page_admin.wait_for_navigation()

        page_admin.assert_success_message()

        from tests.testapp.models import AdvancedStreamFieldPage

        created_page = AdvancedStreamFieldPage.objects.get(title="Deep Nesting Page")
        assert created_page.body[0].block_type == "section"
        assert created_page.body[0].value["heading"] == "Featured Cards"
        assert created_page.body[0].value["cards"][0]["title"] == "Card 1"
        assert (
            created_page.body[0].value["cards"][0]["description"]
            == "First card description"
        )

    def test_deep_nesting_multiple_items(
        self, authenticated_page, server_url, home_page
    ):
        """Test adding multiple items in deeply nested ListBlock."""
        page_admin = PageAdminPage(authenticated_page, server_url)

        url = page_admin.add_child_page_url(
            home_page.id, "testapp", "advancedstreamfieldpage"
        )
        page_admin.goto(url)
        page_admin.wait_for_navigation()

        authenticated_page.locator("#id_title").fill("Multi Card Section")

        sf = StreamFieldHelper(authenticated_page, "body")

        # Add Section block
        index = sf.add_block("Section")
        sf.block(index).struct("heading").fill("Our Team")

        # Fill first card
        sf.block(index).struct("cards").item(0).struct("title").fill("Alice")
        sf.block(index).struct("cards").item(0).struct("description").fill("Developer")

        # Add second card
        sf.block(index).struct("cards").add_item()
        sf.block(index).struct("cards").item(1).struct("title").fill("Bob")
        sf.block(index).struct("cards").item(1).struct("description").fill("Designer")

        # Add third card
        sf.block(index).struct("cards").add_item()
        sf.block(index).struct("cards").item(2).struct("title").fill("Charlie")
        sf.block(index).struct("cards").item(2).struct("description").fill("Manager")

        # Verify item count in nested ListBlock
        assert sf.block(index).struct("cards").item_count() == 3

        # Save
        authenticated_page.get_by_role("tab", name="Promote").click()
        authenticated_page.locator("#id_slug").fill("multi-card-section")
        authenticated_page.get_by_role("button", name="Save draft").click()
        page_admin.wait_for_navigation()

        page_admin.assert_success_message()

        from tests.testapp.models import AdvancedStreamFieldPage

        created_page = AdvancedStreamFieldPage.objects.get(title="Multi Card Section")
        cards = created_page.body[0].value["cards"]
        assert len(cards) == 3
        assert cards[0]["title"] == "Alice"
        assert cards[1]["title"] == "Bob"
        assert cards[2]["title"] == "Charlie"


@pytest.mark.e2e
@pytest.mark.django_db(transaction=True)
class TestStreamFieldHelperValueMethodE2E:
    """E2E tests for value() method across different block types."""

    def test_value_method_simple_block(self, authenticated_page, server_url, home_page):
        """Test value() on simple CharBlock."""
        page_admin = PageAdminPage(authenticated_page, server_url)

        url = page_admin.add_child_page_url(
            home_page.id, "testapp", "advancedstreamfieldpage"
        )
        page_admin.goto(url)
        page_admin.wait_for_navigation()

        sf = StreamFieldHelper(authenticated_page, "body")

        index = sf.add_block("Heading")
        sf.block(index).fill("Test Heading")

        # Verify value() returns what was filled
        assert sf.block(index).value() == "Test Heading"

    def test_value_method_struct_block(self, authenticated_page, server_url, home_page):
        """Test value() on StructBlock fields."""
        page_admin = PageAdminPage(authenticated_page, server_url)

        url = page_admin.add_child_page_url(
            home_page.id, "testapp", "advancedstreamfieldpage"
        )
        page_admin.goto(url)
        page_admin.wait_for_navigation()

        sf = StreamFieldHelper(authenticated_page, "body")

        index = sf.add_block("Hero Section")
        sf.block(index).struct("title").fill("Hero Title")
        sf.block(index).struct("subtitle").fill("Hero Subtitle")

        # Verify values
        assert sf.block(index).struct("title").value() == "Hero Title"
        assert sf.block(index).struct("subtitle").value() == "Hero Subtitle"

    def test_value_method_list_block(self, authenticated_page, server_url, home_page):
        """Test value() on ListBlock items."""
        page_admin = PageAdminPage(authenticated_page, server_url)

        url = page_admin.add_child_page_url(
            home_page.id, "testapp", "advancedstreamfieldpage"
        )
        page_admin.goto(url)
        page_admin.wait_for_navigation()

        sf = StreamFieldHelper(authenticated_page, "body")

        index = sf.add_block("Items")
        sf.block(index).item(0).fill("Item One")

        sf.block(index).add_item()
        sf.block(index).item(1).fill("Item Two")

        # Verify values
        assert sf.block(index).item(0).value() == "Item One"
        assert sf.block(index).item(1).value() == "Item Two"

    def test_value_method_deep_nesting(self, authenticated_page, server_url, home_page):
        """Test value() on deeply nested fields."""
        page_admin = PageAdminPage(authenticated_page, server_url)

        url = page_admin.add_child_page_url(
            home_page.id, "testapp", "advancedstreamfieldpage"
        )
        page_admin.goto(url)
        page_admin.wait_for_navigation()

        sf = StreamFieldHelper(authenticated_page, "body")

        index = sf.add_block("Section")
        sf.block(index).struct("heading").fill("Section Heading")
        sf.block(index).struct("cards").item(0).struct("title").fill("Card Title")
        sf.block(index).struct("cards").item(0).struct("description").fill(
            "Card Description"
        )

        # Verify deeply nested values
        assert sf.block(index).struct("heading").value() == "Section Heading"
        assert (
            sf.block(index).struct("cards").item(0).struct("title").value()
            == "Card Title"
        )
        assert (
            sf.block(index).struct("cards").item(0).struct("description").value()
            == "Card Description"
        )


@pytest.mark.e2e
@pytest.mark.django_db(transaction=True)
class TestStreamFieldHelperComplexScenarioE2E:
    """E2E tests for complex real-world scenarios."""

    def test_full_page_with_all_block_types(
        self, authenticated_page, server_url, home_page
    ):
        """Test creating a page with all available block types."""
        page_admin = PageAdminPage(authenticated_page, server_url)

        url = page_admin.add_child_page_url(
            home_page.id, "testapp", "advancedstreamfieldpage"
        )
        page_admin.goto(url)
        page_admin.wait_for_navigation()

        authenticated_page.locator("#id_title").fill("Complete Page")

        sf = StreamFieldHelper(authenticated_page, "body")

        # 1. Add Heading (simple CharBlock)
        heading_idx = sf.add_block("Heading")
        sf.block(heading_idx).fill("Welcome to Our Website")

        # 2. Add Quote (TextBlock)
        quote_idx = sf.add_block("Quote")
        sf.block(quote_idx).fill("Innovation distinguishes leaders from followers.")

        # 3. Add Hero Section (StructBlock)
        hero_idx = sf.add_block("Hero Section")
        sf.block(hero_idx).struct("title").fill("Main Hero")
        sf.block(hero_idx).struct("subtitle").fill("Your journey starts here")

        # 4. Add Links (ListBlock > StructBlock)
        links_idx = sf.add_block("Links")
        sf.block(links_idx).item(0).struct("title").fill("Documentation")
        sf.block(links_idx).item(0).struct("url").fill("https://docs.example.com")
        sf.block(links_idx).add_item()
        sf.block(links_idx).item(1).struct("title").fill("Support")
        sf.block(links_idx).item(1).struct("url").fill("https://support.example.com")

        # 5. Add Items (ListBlock > CharBlock)
        items_idx = sf.add_block("Items")
        sf.block(items_idx).item(0).fill("Feature 1")
        sf.block(items_idx).add_item()
        sf.block(items_idx).item(1).fill("Feature 2")
        sf.block(items_idx).add_item()
        sf.block(items_idx).item(2).fill("Feature 3")

        # 6. Add Section (StructBlock > ListBlock > StructBlock)
        section_idx = sf.add_block("Section")
        sf.block(section_idx).struct("heading").fill("Team Members")
        sf.block(section_idx).struct("cards").item(0).struct("title").fill("John Doe")
        sf.block(section_idx).struct("cards").item(0).struct("description").fill("CEO")
        sf.block(section_idx).struct("cards").add_item()
        sf.block(section_idx).struct("cards").item(1).struct("title").fill("Jane Doe")
        sf.block(section_idx).struct("cards").item(1).struct("description").fill("CTO")

        # Verify block count
        assert sf.get_block_count() == 6

        # Save
        authenticated_page.get_by_role("tab", name="Promote").click()
        authenticated_page.locator("#id_slug").fill("complete-page")
        authenticated_page.get_by_role("button", name="Save draft").click()
        page_admin.wait_for_navigation()

        page_admin.assert_success_message()

        # Verify all content was saved correctly
        from tests.testapp.models import AdvancedStreamFieldPage

        created_page = AdvancedStreamFieldPage.objects.get(title="Complete Page")

        # Check all blocks
        assert len(created_page.body) == 6

        # Heading
        assert created_page.body[0].block_type == "heading"
        assert created_page.body[0].value == "Welcome to Our Website"

        # Quote
        assert created_page.body[1].block_type == "quote"
        assert "Innovation" in created_page.body[1].value

        # Hero
        assert created_page.body[2].block_type == "hero"
        assert created_page.body[2].value["title"] == "Main Hero"

        # Links
        assert created_page.body[3].block_type == "links"
        assert len(created_page.body[3].value) == 2
        assert created_page.body[3].value[0]["title"] == "Documentation"

        # Items
        assert created_page.body[4].block_type == "items"
        assert len(created_page.body[4].value) == 3
        assert created_page.body[4].value[0] == "Feature 1"

        # Section (deep nesting)
        assert created_page.body[5].block_type == "section"
        assert created_page.body[5].value["heading"] == "Team Members"
        assert len(created_page.body[5].value["cards"]) == 2
        assert created_page.body[5].value["cards"][0]["title"] == "John Doe"
        assert created_page.body[5].value["cards"][1]["title"] == "Jane Doe"


@pytest.mark.e2e
@pytest.mark.django_db(transaction=True)
class TestStreamFieldHelperImageChooserE2E:
    """E2E tests for ImageChooserBlock with click_chooser and select_from_chooser."""

    def test_click_chooser_opens_modal(
        self, authenticated_page, server_url, home_page, test_image
    ):
        """Test that click_chooser opens the image chooser modal."""
        page_admin = PageAdminPage(authenticated_page, server_url)

        url = page_admin.add_child_page_url(
            home_page.id, "testapp", "advancedstreamfieldpage"
        )
        page_admin.goto(url)
        page_admin.wait_for_navigation()

        authenticated_page.locator("#id_title").fill("Image Chooser Test Page")

        sf = StreamFieldHelper(authenticated_page, "body")

        # Add standalone Image block
        index = sf.add_block("Image")

        # Click chooser button
        sf.block(index).click_chooser()

        # Verify modal is open by checking for modal elements
        # Wagtail's image chooser modal has specific UI elements
        modal = authenticated_page.locator("[data-chooser-modal], .modal")
        assert modal.count() > 0, "Image chooser modal should be open"

    def test_select_image_from_chooser(
        self, authenticated_page, server_url, home_page, test_image
    ):
        """Test selecting an image from the chooser modal."""
        page_admin = PageAdminPage(authenticated_page, server_url)

        url = page_admin.add_child_page_url(
            home_page.id, "testapp", "advancedstreamfieldpage"
        )
        page_admin.goto(url)
        page_admin.wait_for_navigation()

        authenticated_page.locator("#id_title").fill("Select Image Test Page")

        sf = StreamFieldHelper(authenticated_page, "body")

        # Add standalone Image block
        index = sf.add_block("Image")

        # Click chooser and select image
        sf.block(index).click_chooser()
        sf.select_from_chooser(test_image.title)

        # Wait for chooser to close
        authenticated_page.wait_for_timeout(500)

        # Modal should be closed (check using Bootstrap modal selector)
        modal = authenticated_page.locator(".modal.fade.in")
        assert modal.count() == 0, "Modal should be closed after selection"

    def test_image_in_struct_block(
        self, authenticated_page, server_url, home_page, test_image
    ):
        """Test ImageChooserBlock inside a StructBlock (HeroBlock)."""
        page_admin = PageAdminPage(authenticated_page, server_url)

        url = page_admin.add_child_page_url(
            home_page.id, "testapp", "advancedstreamfieldpage"
        )
        page_admin.goto(url)
        page_admin.wait_for_navigation()

        authenticated_page.locator("#id_title").fill("Hero With Image Page")

        sf = StreamFieldHelper(authenticated_page, "body")

        # Add Hero Section block (has optional image field)
        index = sf.add_block("Hero Section")

        # Fill text fields
        sf.block(index).struct("title").fill("Welcome Hero")
        sf.block(index).struct("subtitle").fill("With an image")

        # Select image using fluent API
        sf.block(index).struct("image").click_chooser()
        sf.select_from_chooser(test_image.title)

        # Wait for selection
        authenticated_page.wait_for_timeout(500)

        # Save the page
        authenticated_page.get_by_role("tab", name="Promote").click()
        authenticated_page.locator("#id_slug").fill("hero-with-image")
        authenticated_page.get_by_role("button", name="Save draft").click()
        page_admin.wait_for_navigation()

        page_admin.assert_success_message()

        # Verify the image was saved
        from tests.testapp.models import AdvancedStreamFieldPage

        created_page = AdvancedStreamFieldPage.objects.get(title="Hero With Image Page")
        assert created_page.body[0].block_type == "hero"
        assert created_page.body[0].value["title"] == "Welcome Hero"
        # Image should be set
        assert created_page.body[0].value["image"] is not None
        assert created_page.body[0].value["image"].title == test_image.title

    def test_save_page_with_standalone_image(
        self, authenticated_page, server_url, home_page, test_image
    ):
        """Test saving a page with a standalone ImageChooserBlock."""
        page_admin = PageAdminPage(authenticated_page, server_url)

        url = page_admin.add_child_page_url(
            home_page.id, "testapp", "advancedstreamfieldpage"
        )
        page_admin.goto(url)
        page_admin.wait_for_navigation()

        authenticated_page.locator("#id_title").fill("Standalone Image Page")

        sf = StreamFieldHelper(authenticated_page, "body")

        # Add standalone Image block
        index = sf.add_block("Image")

        # Select image
        sf.block(index).click_chooser()
        sf.select_from_chooser(test_image.title)

        # Wait for selection
        authenticated_page.wait_for_timeout(500)

        # Save the page
        authenticated_page.get_by_role("tab", name="Promote").click()
        authenticated_page.locator("#id_slug").fill("standalone-image")
        authenticated_page.get_by_role("button", name="Save draft").click()
        page_admin.wait_for_navigation()

        page_admin.assert_success_message()

        # Verify the image was saved
        from tests.testapp.models import AdvancedStreamFieldPage

        created_page = AdvancedStreamFieldPage.objects.get(
            title="Standalone Image Page"
        )
        assert created_page.body[0].block_type == "image"
        assert created_page.body[0].value is not None
        assert created_page.body[0].value.title == test_image.title


@pytest.mark.e2e
@pytest.mark.django_db(transaction=True)
class TestStreamFieldHelperSnippetChooserE2E:
    """E2E tests for SnippetChooserBlock with click_chooser and select_from_chooser."""

    def test_click_chooser_opens_snippet_modal(
        self, authenticated_page, server_url, home_page, test_snippet
    ):
        """Test that click_chooser opens the snippet chooser modal."""
        page_admin = PageAdminPage(authenticated_page, server_url)

        url = page_admin.add_child_page_url(
            home_page.id, "testapp", "advancedstreamfieldpage"
        )
        page_admin.goto(url)
        page_admin.wait_for_navigation()

        authenticated_page.locator("#id_title").fill("Snippet Chooser Test Page")

        sf = StreamFieldHelper(authenticated_page, "body")

        # Add Snippet block
        index = sf.add_block("Snippet")

        # Click chooser button
        sf.block(index).click_chooser()

        # Verify modal is open
        modal = authenticated_page.locator(".modal")
        assert modal.count() > 0, "Snippet chooser modal should be open"

    def test_select_snippet_from_chooser(
        self, authenticated_page, server_url, home_page, test_snippet
    ):
        """Test selecting a snippet from the chooser modal."""
        page_admin = PageAdminPage(authenticated_page, server_url)

        url = page_admin.add_child_page_url(
            home_page.id, "testapp", "advancedstreamfieldpage"
        )
        page_admin.goto(url)
        page_admin.wait_for_navigation()

        authenticated_page.locator("#id_title").fill("Select Snippet Test Page")

        sf = StreamFieldHelper(authenticated_page, "body")

        # Add Snippet block
        index = sf.add_block("Snippet")

        # Click chooser and select snippet
        sf.block(index).click_chooser()
        sf.select_from_chooser(test_snippet.name)

        # Wait for chooser to close
        authenticated_page.wait_for_timeout(500)

        # Modal should be closed
        modal = authenticated_page.locator(".modal.fade.in")
        assert modal.count() == 0, "Modal should be closed after selection"

    def test_save_page_with_snippet(
        self, authenticated_page, server_url, home_page, test_snippet
    ):
        """Test saving a page with a SnippetChooserBlock."""
        page_admin = PageAdminPage(authenticated_page, server_url)

        url = page_admin.add_child_page_url(
            home_page.id, "testapp", "advancedstreamfieldpage"
        )
        page_admin.goto(url)
        page_admin.wait_for_navigation()

        authenticated_page.locator("#id_title").fill("Page With Snippet")

        sf = StreamFieldHelper(authenticated_page, "body")

        # Add Snippet block
        index = sf.add_block("Snippet")

        # Select snippet
        sf.block(index).click_chooser()
        sf.select_from_chooser(test_snippet.name)

        authenticated_page.wait_for_timeout(500)

        # Save the page
        authenticated_page.get_by_role("tab", name="Promote").click()
        authenticated_page.locator("#id_slug").fill("page-with-snippet")
        authenticated_page.get_by_role("button", name="Save draft").click()
        page_admin.wait_for_navigation()

        page_admin.assert_success_message()

        # Verify the snippet was saved
        from tests.testapp.models import AdvancedStreamFieldPage

        created_page = AdvancedStreamFieldPage.objects.get(title="Page With Snippet")
        assert created_page.body[0].block_type == "snippet"
        assert created_page.body[0].value is not None
        assert created_page.body[0].value.name == test_snippet.name


@pytest.mark.e2e
@pytest.mark.django_db(transaction=True)
class TestStreamFieldHelperPageChooserE2E:
    """E2E tests for PageChooserBlock with click_chooser and select_from_chooser."""

    def test_click_chooser_opens_page_modal(
        self, authenticated_page, server_url, home_page, test_related_page
    ):
        """Test that click_chooser opens the page chooser modal."""
        page_admin = PageAdminPage(authenticated_page, server_url)

        url = page_admin.add_child_page_url(
            home_page.id, "testapp", "advancedstreamfieldpage"
        )
        page_admin.goto(url)
        page_admin.wait_for_navigation()

        authenticated_page.locator("#id_title").fill("Page Chooser Test Page")

        sf = StreamFieldHelper(authenticated_page, "body")

        # Add Related page block
        index = sf.add_block("Related page")

        # Click chooser button
        sf.block(index).click_chooser()

        # Verify modal is open
        modal = authenticated_page.locator(".modal")
        assert modal.count() > 0, "Page chooser modal should be open"

    def test_select_page_from_chooser(self, authenticated_page, server_url, home_page):
        """Test selecting a page from the chooser modal.

        Note: PageChooser shows a hierarchical view. This test selects the
        home page which is directly visible in the chooser without navigation.
        """
        page_admin = PageAdminPage(authenticated_page, server_url)

        url = page_admin.add_child_page_url(
            home_page.id, "testapp", "advancedstreamfieldpage"
        )
        page_admin.goto(url)
        page_admin.wait_for_navigation()

        authenticated_page.locator("#id_title").fill("Select Page Test Page")

        sf = StreamFieldHelper(authenticated_page, "body")

        # Add Related page block
        index = sf.add_block("Related page")

        # Click chooser and select the home page (directly visible)
        sf.block(index).click_chooser()
        sf.select_from_chooser(home_page.title)

        # Wait for chooser to close
        authenticated_page.wait_for_timeout(500)

        # Modal should be closed
        modal = authenticated_page.locator(".modal.fade.in")
        assert modal.count() == 0, "Modal should be closed after selection"

    def test_save_page_with_related_page(
        self, authenticated_page, server_url, home_page
    ):
        """Test saving a page with a PageChooserBlock."""
        page_admin = PageAdminPage(authenticated_page, server_url)

        url = page_admin.add_child_page_url(
            home_page.id, "testapp", "advancedstreamfieldpage"
        )
        page_admin.goto(url)
        page_admin.wait_for_navigation()

        authenticated_page.locator("#id_title").fill("Page With Related Page")

        sf = StreamFieldHelper(authenticated_page, "body")

        # Add Related page block
        index = sf.add_block("Related page")

        # Select the home page (directly visible in chooser)
        sf.block(index).click_chooser()
        sf.select_from_chooser(home_page.title)

        authenticated_page.wait_for_timeout(500)

        # Save the page
        authenticated_page.get_by_role("tab", name="Promote").click()
        authenticated_page.locator("#id_slug").fill("page-with-related-page")
        authenticated_page.get_by_role("button", name="Save draft").click()
        page_admin.wait_for_navigation()

        page_admin.assert_success_message()

        # Verify the related page was saved
        from tests.testapp.models import AdvancedStreamFieldPage

        created_page = AdvancedStreamFieldPage.objects.get(
            title="Page With Related Page"
        )
        assert created_page.body[0].block_type == "related_page"
        assert created_page.body[0].value is not None
        assert created_page.body[0].value.title == home_page.title
