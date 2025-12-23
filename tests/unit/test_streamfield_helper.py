"""Tests for StreamFieldHelper and BlockPath."""

from unittest.mock import MagicMock

from wagtail_scenario_test import BlockPath, StreamFieldHelper


class TestStreamFieldHelperInit:
    """Tests for StreamFieldHelper initialization."""

    def test_init_with_default_field_name(self):
        """StreamFieldHelper should default to 'body' field name."""
        mock_page = MagicMock()
        helper = StreamFieldHelper(mock_page)

        assert helper.page is mock_page
        assert helper.field_name == "body"

    def test_init_with_custom_field_name(self):
        """StreamFieldHelper should accept custom field name."""
        mock_page = MagicMock()
        helper = StreamFieldHelper(mock_page, "content")

        assert helper.field_name == "content"


class TestStreamFieldHelperAddBlock:
    """Tests for StreamFieldHelper.add_block()."""

    def test_add_block_clicks_add_button(self):
        """add_block should click the add button."""
        mock_page = MagicMock()
        mock_panel = MagicMock()
        mock_add_button = MagicMock()
        mock_option = MagicMock()
        mock_count_input = MagicMock()

        # Setup mock chain
        mock_page.locator.side_effect = [
            mock_count_input,  # For _get_block_count
            mock_panel,  # For panel selector
            MagicMock(),  # For menu wait
            mock_option,  # For option filter
        ]
        mock_panel.locator.return_value.first = mock_add_button
        mock_count_input.count.return_value = 1
        mock_count_input.input_value.return_value = "0"
        mock_option.first = mock_option

        helper = StreamFieldHelper(mock_page, "body")
        helper.add_block("Heading")

        mock_add_button.click.assert_called_once()

    def test_add_block_selects_block_type(self):
        """add_block should select the correct block type."""
        mock_page = MagicMock()
        mock_panel = MagicMock()
        mock_option = MagicMock()
        mock_count_input = MagicMock()
        mock_menu = MagicMock()
        mock_options_locator = MagicMock()

        # Setup mock chain
        mock_page.locator.side_effect = [
            mock_count_input,  # For _get_block_count
            mock_panel,  # For panel selector
            mock_menu,  # For menu wait
            mock_options_locator,  # For option filter
        ]
        mock_panel.locator.return_value.first = MagicMock()
        mock_count_input.count.return_value = 1
        mock_count_input.input_value.return_value = "0"
        mock_options_locator.filter.return_value = mock_option
        mock_option.first = mock_option

        helper = StreamFieldHelper(mock_page, "body")
        helper.add_block("Heading")

        mock_options_locator.filter.assert_called_once_with(has_text="Heading")
        mock_option.click.assert_called_once()

    def test_add_block_returns_block_index(self):
        """add_block should return the index of the new block."""
        mock_page = MagicMock()
        mock_panel = MagicMock()
        mock_option = MagicMock()
        mock_count_input = MagicMock()
        mock_menu = MagicMock()
        mock_options_locator = MagicMock()

        # Setup: pretend there's already 2 blocks
        mock_page.locator.side_effect = [
            mock_count_input,  # For _get_block_count
            mock_panel,  # For panel selector
            mock_menu,  # For menu wait
            mock_options_locator,  # For option filter
        ]
        mock_panel.locator.return_value.first = MagicMock()
        mock_count_input.count.return_value = 1
        mock_count_input.input_value.return_value = "2"  # 2 existing blocks
        mock_options_locator.filter.return_value = mock_option
        mock_option.first = mock_option

        helper = StreamFieldHelper(mock_page, "body")
        index = helper.add_block("Quote")

        assert index == 2  # New block gets index 2


class TestStreamFieldHelperGetBlockCount:
    """Tests for StreamFieldHelper.get_block_count()."""

    def test_get_block_count_returns_count(self):
        """get_block_count should return the number of blocks."""
        mock_page = MagicMock()
        mock_count_input = MagicMock()
        mock_count_input.count.return_value = 1
        mock_count_input.input_value.return_value = "3"

        mock_page.locator.return_value = mock_count_input

        helper = StreamFieldHelper(mock_page, "body")
        count = helper.get_block_count()

        assert count == 3
        mock_page.locator.assert_called_with("input[name='body-count']")

    def test_get_block_count_returns_zero_when_no_input(self):
        """get_block_count should return 0 when count input not found."""
        mock_page = MagicMock()
        mock_count_input = MagicMock()
        mock_count_input.count.return_value = 0

        mock_page.locator.return_value = mock_count_input

        helper = StreamFieldHelper(mock_page, "body")
        count = helper.get_block_count()

        assert count == 0


class TestStreamFieldHelperGetBlockType:
    """Tests for StreamFieldHelper.get_block_type()."""

    def test_get_block_type_returns_type(self):
        """get_block_type should return the block type."""
        mock_page = MagicMock()
        mock_type_input = MagicMock()
        mock_type_input.input_value.return_value = "heading"

        mock_page.locator.return_value = mock_type_input

        helper = StreamFieldHelper(mock_page, "body")
        block_type = helper.get_block_type(0)

        assert block_type == "heading"
        mock_page.locator.assert_called_with("input[name='body-0-type']")

    def test_get_block_type_with_different_index(self):
        """get_block_type should use correct index in selector."""
        mock_page = MagicMock()
        mock_type_input = MagicMock()
        mock_type_input.input_value.return_value = "paragraph"

        mock_page.locator.return_value = mock_type_input

        helper = StreamFieldHelper(mock_page, "content")
        block_type = helper.get_block_type(5)

        assert block_type == "paragraph"
        mock_page.locator.assert_called_with("input[name='content-5-type']")


class TestBlockPathNavigation:
    """Tests for BlockPath navigation methods."""

    def test_block_returns_blockpath(self):
        """block() should return a BlockPath instance."""
        mock_page = MagicMock()
        helper = StreamFieldHelper(mock_page, "body")

        path = helper.block(0)

        assert isinstance(path, BlockPath)
        assert path._id == "body-0"

    def test_struct_from_block(self):
        """struct() from block should add -value-{field}."""
        mock_page = MagicMock()
        helper = StreamFieldHelper(mock_page, "body")

        path = helper.block(0).struct("title")

        assert path._id == "body-0-value-title"

    def test_struct_from_item(self):
        """struct() after item() should just add -{field}."""
        mock_page = MagicMock()
        helper = StreamFieldHelper(mock_page, "body")

        path = helper.block(0).item(0).struct("title")

        assert path._id == "body-0-value-0-value-title"

    def test_item_from_block(self):
        """item() from block should add -value-{index}-value."""
        mock_page = MagicMock()
        helper = StreamFieldHelper(mock_page, "body")

        path = helper.block(0).item(0)

        assert path._id == "body-0-value-0-value"

    def test_item_from_struct(self):
        """item() after struct() should add -{index}-value."""
        mock_page = MagicMock()
        helper = StreamFieldHelper(mock_page, "body")

        path = helper.block(0).item(0).struct("cards").item(0)

        assert path._id == "body-0-value-0-value-cards-0-value"

    def test_deep_nesting(self):
        """Deep nesting should build correct path."""
        mock_page = MagicMock()
        helper = StreamFieldHelper(mock_page, "body")

        # Deep nesting: block -> item -> struct -> item -> struct -> item -> struct
        path = (
            helper.block(0)
            .item(0)
            .struct("sections")
            .item(0)
            .struct("cards")
            .item(0)
            .struct("title")
        )

        expected = "body-0-value-0-value-sections-0-value-cards-0-value-title"
        assert path._id == expected


class TestBlockPathFill:
    """Tests for BlockPath.fill()."""

    def test_fill_simple_block(self):
        """fill() on simple block should use correct selector."""
        mock_page = MagicMock()
        mock_field = MagicMock()
        mock_field.count.return_value = 1

        mock_page.locator.return_value = mock_field

        helper = StreamFieldHelper(mock_page, "body")
        helper.block(0).fill("Test Value")

        mock_page.locator.assert_called_with("#body-0-value")
        mock_field.fill.assert_called_once_with("Test Value")

    def test_fill_struct_field(self):
        """fill() on struct field should use correct selector."""
        mock_page = MagicMock()
        mock_field = MagicMock()
        mock_field.count.return_value = 1

        mock_page.locator.return_value = mock_field

        helper = StreamFieldHelper(mock_page, "body")
        helper.block(0).struct("title").fill("Welcome")

        mock_page.locator.assert_called_with("#body-0-value-title")
        mock_field.fill.assert_called_once_with("Welcome")

    def test_fill_list_item(self):
        """fill() on list item should use correct selector."""
        mock_page = MagicMock()
        mock_field = MagicMock()
        mock_field.count.return_value = 1

        mock_page.locator.return_value = mock_field

        helper = StreamFieldHelper(mock_page, "body")
        helper.block(0).item(0).fill("First item")

        mock_page.locator.assert_called_with("#body-0-value-0-value")
        mock_field.fill.assert_called_once_with("First item")

    def test_fill_list_item_struct_field(self):
        """fill() on list item struct field should use correct selector."""
        mock_page = MagicMock()
        mock_field = MagicMock()
        mock_field.count.return_value = 1

        mock_page.locator.return_value = mock_field

        helper = StreamFieldHelper(mock_page, "content")
        helper.block(1).item(2).struct("url").fill("https://example.com")

        mock_page.locator.assert_called_with("#content-1-value-2-value-url")
        mock_field.fill.assert_called_once_with("https://example.com")


class TestBlockPathValue:
    """Tests for BlockPath.value()."""

    def test_value_returns_field_value(self):
        """value() should return the field's current value."""
        mock_page = MagicMock()
        mock_field = MagicMock()
        mock_field.count.return_value = 1
        mock_field.input_value.return_value = "Current value"

        mock_page.locator.return_value = mock_field

        helper = StreamFieldHelper(mock_page, "body")
        value = helper.block(0).struct("title").value()

        assert value == "Current value"
        mock_page.locator.assert_called_with("#body-0-value-title")

    def test_value_returns_empty_when_not_found(self):
        """value() should return empty string when field not found."""
        mock_page = MagicMock()
        mock_field = MagicMock()
        mock_field.count.return_value = 0

        mock_page.locator.return_value = mock_field

        helper = StreamFieldHelper(mock_page, "body")
        value = helper.block(0).struct("nonexistent").value()

        assert value == ""


class TestBlockPathItemCount:
    """Tests for BlockPath.item_count()."""

    def test_item_count_returns_count(self):
        """item_count() should return number of items."""
        mock_page = MagicMock()
        mock_count_input = MagicMock()
        mock_count_input.count.return_value = 1
        mock_count_input.input_value.return_value = "3"

        mock_page.locator.return_value = mock_count_input

        helper = StreamFieldHelper(mock_page, "body")
        count = helper.block(0).item_count()

        assert count == 3
        mock_page.locator.assert_called_with("input[name='body-0-value-count']")

    def test_item_count_returns_zero_when_no_input(self):
        """item_count() should return 0 when count input not found."""
        mock_page = MagicMock()
        mock_count_input = MagicMock()
        mock_count_input.count.return_value = 0

        mock_page.locator.return_value = mock_count_input

        helper = StreamFieldHelper(mock_page, "body")
        count = helper.block(0).item_count()

        assert count == 0


class TestBlockPathClickChooser:
    """Tests for BlockPath.click_chooser()."""

    def test_click_chooser_standalone(self):
        """click_chooser() on standalone block should click button."""
        mock_page = MagicMock()
        mock_button = MagicMock()
        mock_button.count.return_value = 1

        mock_page.locator.return_value.first = mock_button

        helper = StreamFieldHelper(mock_page, "body")
        helper.block(0).click_chooser()

        mock_button.click.assert_called_once()

    def test_click_chooser_in_struct(self):
        """click_chooser() on struct field should use correct selector."""
        mock_page = MagicMock()
        mock_button = MagicMock()
        mock_button.count.return_value = 1

        mock_page.locator.return_value.first = mock_button

        helper = StreamFieldHelper(mock_page, "body")
        helper.block(0).struct("image").click_chooser()

        # Verify locator was called with the struct field context
        mock_page.locator.assert_called()
        call_args = mock_page.locator.call_args[0][0]
        assert "body-0-value-image" in call_args


class TestLegacyMethods:
    """Tests for backward-compatible legacy methods."""

    def test_fill_block_calls_fluent_api(self):
        """fill_block() should delegate to block().fill()."""
        mock_page = MagicMock()
        mock_field = MagicMock()
        mock_field.count.return_value = 1
        mock_page.locator.return_value = mock_field

        helper = StreamFieldHelper(mock_page, "body")
        helper.fill_block(0, "Test Value")

        mock_page.locator.assert_called_with("#body-0-value")
        mock_field.fill.assert_called_once_with("Test Value")

    def test_fill_struct_field_calls_fluent_api(self):
        """fill_struct_field() should delegate to block().struct().fill()."""
        mock_page = MagicMock()
        mock_field = MagicMock()
        mock_field.count.return_value = 1
        mock_page.locator.return_value = mock_field

        helper = StreamFieldHelper(mock_page, "body")
        helper.fill_struct_field(0, "title", "Welcome")

        mock_page.locator.assert_called_with("#body-0-value-title")
        mock_field.fill.assert_called_once_with("Welcome")

    def test_fill_list_item_field_calls_fluent_api(self):
        """fill_list_item_field() should delegate to fluent API."""
        mock_page = MagicMock()
        mock_field = MagicMock()
        mock_field.count.return_value = 1
        mock_page.locator.return_value = mock_field

        helper = StreamFieldHelper(mock_page, "body")
        helper.fill_list_item_field(0, 0, "title", "Link Title")

        mock_page.locator.assert_called_with("#body-0-value-0-value-title")
        mock_field.fill.assert_called_once_with("Link Title")

    def test_get_struct_field_value_calls_fluent_api(self):
        """get_struct_field_value() should delegate to fluent API."""
        mock_page = MagicMock()
        mock_field = MagicMock()
        mock_field.count.return_value = 1
        mock_field.input_value.return_value = "Current value"
        mock_page.locator.return_value = mock_field

        helper = StreamFieldHelper(mock_page, "body")
        value = helper.get_struct_field_value(0, "title")

        assert value == "Current value"
        mock_page.locator.assert_called_with("#body-0-value-title")

    def test_get_list_item_field_value_calls_fluent_api(self):
        """get_list_item_field_value() should delegate to fluent API."""
        mock_page = MagicMock()
        mock_field = MagicMock()
        mock_field.count.return_value = 1
        mock_field.input_value.return_value = "https://google.com"
        mock_page.locator.return_value = mock_field

        helper = StreamFieldHelper(mock_page, "body")
        value = helper.get_list_item_field_value(0, 0, "url")

        assert value == "https://google.com"
        mock_page.locator.assert_called_with("#body-0-value-0-value-url")
