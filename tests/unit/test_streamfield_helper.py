"""Tests for StreamFieldHelper."""

from unittest.mock import MagicMock

from wagtail_scenario_test import StreamFieldHelper


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


class TestStreamFieldHelperFillBlock:
    """Tests for StreamFieldHelper.fill_block()."""

    def test_fill_block_fills_input(self):
        """fill_block should fill input field."""
        mock_page = MagicMock()
        mock_input = MagicMock()
        mock_input.count.return_value = 1

        mock_page.locator.return_value = mock_input

        helper = StreamFieldHelper(mock_page, "body")
        helper.fill_block(0, "Test Value")

        mock_page.locator.assert_called_with("#body-0-value")
        mock_input.fill.assert_called_once_with("Test Value")

    def test_fill_block_with_custom_field_name(self):
        """fill_block should use correct field name in selector."""
        mock_page = MagicMock()
        mock_input = MagicMock()
        mock_input.count.return_value = 1

        mock_page.locator.return_value = mock_input

        helper = StreamFieldHelper(mock_page, "content")
        helper.fill_block(3, "Custom Value")

        mock_page.locator.assert_called_with("#content-3-value")


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
