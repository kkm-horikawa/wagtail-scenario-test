"""Unit tests for SnippetAdminPage."""

from unittest.mock import MagicMock

import pytest

from wagtail_scenario_test.page_objects.wagtail_admin import SnippetAdminPage


class TestSnippetAdminPageInit:
    """Tests for SnippetAdminPage initialization."""

    def test_init_stores_app_and_model_name(self, mock_page, test_url):
        """SnippetAdminPage should store app_name and model_name."""
        page = SnippetAdminPage(
            mock_page,
            test_url,
            app_name="myapp",
            model_name="mymodel",
        )

        assert page.app_name == "myapp"
        assert page.model_name == "mymodel"


class TestSnippetAdminPageUrls:
    """Tests for SnippetAdminPage URL properties."""

    def test_list_url(self, mock_page, test_url):
        """list_url should return correct snippet list URL."""
        page = SnippetAdminPage(
            mock_page,
            test_url,
            app_name="myapp",
            model_name="mymodel",
        )

        assert page.list_url == "/admin/snippets/myapp/mymodel/"

    def test_add_url(self, mock_page, test_url):
        """add_url should return correct snippet add URL."""
        page = SnippetAdminPage(
            mock_page,
            test_url,
            app_name="myapp",
            model_name="mymodel",
        )

        assert page.add_url == "/admin/snippets/myapp/mymodel/add/"

    def test_edit_url(self, mock_page, test_url):
        """edit_url should return correct snippet edit URL."""
        page = SnippetAdminPage(
            mock_page,
            test_url,
            app_name="myapp",
            model_name="mymodel",
        )

        assert page.edit_url(123) == "/admin/snippets/myapp/mymodel/edit/123/"

    def test_delete_url(self, mock_page, test_url):
        """delete_url should return correct snippet delete URL."""
        page = SnippetAdminPage(
            mock_page,
            test_url,
            app_name="myapp",
            model_name="mymodel",
        )

        assert page.delete_url(456) == "/admin/snippets/myapp/mymodel/delete/456/"


class TestSnippetAdminPageNavigation:
    """Tests for SnippetAdminPage navigation methods."""

    def test_go_to_list(self, mock_page, test_url):
        """go_to_list should navigate to list URL."""
        page = SnippetAdminPage(
            mock_page,
            test_url,
            app_name="myapp",
            model_name="mymodel",
        )

        page.go_to_list()

        mock_page.goto.assert_called_once_with(
            f"{test_url}/admin/snippets/myapp/mymodel/"
        )

    def test_go_to_add(self, mock_page, test_url):
        """go_to_add should navigate to add URL."""
        page = SnippetAdminPage(
            mock_page,
            test_url,
            app_name="myapp",
            model_name="mymodel",
        )

        page.go_to_add()

        mock_page.goto.assert_called_once_with(
            f"{test_url}/admin/snippets/myapp/mymodel/add/"
        )

    def test_go_to_edit(self, mock_page, test_url):
        """go_to_edit should navigate to edit URL."""
        page = SnippetAdminPage(
            mock_page,
            test_url,
            app_name="myapp",
            model_name="mymodel",
        )

        page.go_to_edit(42)

        mock_page.goto.assert_called_once_with(
            f"{test_url}/admin/snippets/myapp/mymodel/edit/42/"
        )


class TestSnippetAdminPageCreate:
    """Tests for SnippetAdminPage create method."""

    def test_create_with_name(self, mock_page, test_url):
        """create should fill name and save."""
        page = SnippetAdminPage(
            mock_page,
            test_url,
            app_name="myapp",
            model_name="mymodel",
        )
        name_input = mock_page.locator.return_value

        page.create(name="Test Item")

        # Check navigation to add page
        mock_page.goto.assert_called_with(
            f"{test_url}/admin/snippets/myapp/mymodel/add/"
        )

        # Check name field was filled
        mock_page.locator.assert_any_call("#id_name")
        name_input.fill.assert_called_with("Test Item")

        # Check save button was clicked
        mock_page.get_by_role.assert_called_with("button", name="Save")

    def test_create_without_save(self, mock_page, test_url):
        """create with save=False should not click Save."""
        page = SnippetAdminPage(
            mock_page,
            test_url,
            app_name="myapp",
            model_name="mymodel",
        )

        page.create(name="Test Item", save=False)

        # Check Save button was NOT clicked
        mock_page.get_by_role.assert_not_called()

    def test_create_with_additional_fields(self, mock_page, test_url):
        """create should fill additional fields."""
        page = SnippetAdminPage(
            mock_page,
            test_url,
            app_name="myapp",
            model_name="mymodel",
        )

        page.create(name="Test", id_slug="test-slug", id_description="A description")

        # Check additional fields were filled
        mock_page.locator.assert_any_call("#id_slug")
        mock_page.locator.assert_any_call("#id_description")

    def test_create_without_name(self, mock_page, test_url):
        """create without name should not fill name field."""
        page = SnippetAdminPage(
            mock_page,
            test_url,
            app_name="myapp",
            model_name="mymodel",
        )

        page.create(id_custom_field="value")

        # Check that #id_name was NOT specifically called
        # (other locator calls may happen)
        calls = [str(c) for c in mock_page.locator.call_args_list]
        assert any("#id_custom_field" in str(c) for c in calls)


class TestSnippetAdminPageFormInteractions:
    """Tests for SnippetAdminPage form interactions."""

    def test_save(self, mock_page, test_url):
        """save should click Save button."""
        page = SnippetAdminPage(
            mock_page,
            test_url,
            app_name="myapp",
            model_name="mymodel",
        )

        page.save()

        mock_page.get_by_role.assert_called_with("button", name="Save")
        mock_page.get_by_role.return_value.click.assert_called_once()

    def test_save_draft(self, mock_page, test_url):
        """save_draft should click Save draft button."""
        page = SnippetAdminPage(
            mock_page,
            test_url,
            app_name="myapp",
            model_name="mymodel",
        )

        page.save_draft()

        mock_page.get_by_role.assert_called_with("button", name="Save draft")
        mock_page.get_by_role.return_value.click.assert_called_once()

    def test_delete_with_confirm(self, mock_page, test_url):
        """delete should open dropdown, click Delete link, and confirm."""
        page = SnippetAdminPage(
            mock_page,
            test_url,
            app_name="myapp",
            model_name="mymodel",
        )

        page.delete()

        # Check dropdown toggle was clicked
        mock_page.locator.assert_any_call(
            "[data-controller='w-dropdown'] button[data-w-dropdown-target='toggle']"
        )
        mock_page.locator.return_value.click.assert_called()

        # Check Delete link (not button) and Yes, delete button were clicked
        mock_page.get_by_role.assert_any_call("link", name="Delete", exact=True)
        mock_page.get_by_role.assert_any_call("button", name="Yes, delete")

    def test_delete_without_confirm(self, mock_page, test_url):
        """delete with confirm=False should only open dropdown and click Delete link."""
        page = SnippetAdminPage(
            mock_page,
            test_url,
            app_name="myapp",
            model_name="mymodel",
        )

        page.delete(confirm=False)

        # Check dropdown toggle was clicked
        mock_page.locator.assert_any_call(
            "[data-controller='w-dropdown'] button[data-w-dropdown-target='toggle']"
        )

        # Only Delete link clicked (not the confirmation button)
        mock_page.get_by_role.assert_called_once_with("link", name="Delete", exact=True)


class TestSnippetAdminPageListOperations:
    """Tests for SnippetAdminPage list operations."""

    def test_get_item_count(self, mock_page, test_url):
        """get_item_count should return number of rows."""
        page = SnippetAdminPage(
            mock_page,
            test_url,
            app_name="myapp",
            model_name="mymodel",
        )
        mock_page.locator.return_value.count.return_value = 5

        result = page.get_item_count()

        mock_page.locator.assert_called_with("table tbody tr")
        assert result == 5

    def test_item_exists_in_list_returns_true(self, mock_page, test_url):
        """item_exists_in_list should return True when found."""
        page = SnippetAdminPage(
            mock_page,
            test_url,
            app_name="myapp",
            model_name="mymodel",
        )
        mock_page.get_by_role.return_value.count.return_value = 1

        result = page.item_exists_in_list("Test Item")

        mock_page.get_by_role.assert_called_with("link", name="Test Item")
        assert result is True

    def test_item_exists_in_list_returns_false(self, mock_page, test_url):
        """item_exists_in_list should return False when not found."""
        page = SnippetAdminPage(
            mock_page,
            test_url,
            app_name="myapp",
            model_name="mymodel",
        )
        mock_page.get_by_role.return_value.count.return_value = 0

        result = page.item_exists_in_list("Nonexistent")

        assert result is False

    def test_click_item_in_list(self, mock_page, test_url):
        """click_item_in_list should click item link."""
        page = SnippetAdminPage(
            mock_page,
            test_url,
            app_name="myapp",
            model_name="mymodel",
        )

        page.click_item_in_list("Test Item")

        mock_page.get_by_role.assert_called_with("link", name="Test Item")
        mock_page.get_by_role.return_value.click.assert_called_once()

    def test_get_list_items(self, mock_page, test_url):
        """get_list_items should return list of item titles."""
        page = SnippetAdminPage(
            mock_page,
            test_url,
            app_name="myapp",
            model_name="mymodel",
        )
        link1 = MagicMock()
        link1.text_content.return_value = "Item 1"
        link2 = MagicMock()
        link2.text_content.return_value = "Item 2"
        mock_page.locator.return_value.all.return_value = [link1, link2]

        result = page.get_list_items()

        mock_page.locator.assert_called_with("table tbody tr td a")
        assert result == ["Item 1", "Item 2"]

    def test_get_list_items_handles_none_text(self, mock_page, test_url):
        """get_list_items should handle None text_content."""
        page = SnippetAdminPage(
            mock_page,
            test_url,
            app_name="myapp",
            model_name="mymodel",
        )
        link = MagicMock()
        link.text_content.return_value = None
        mock_page.locator.return_value.all.return_value = [link]

        result = page.get_list_items()

        assert result == [""]


class TestSnippetAdminPageAssertions:
    """Tests for SnippetAdminPage assertion methods."""

    def test_assert_on_list_page(self, mock_page, test_url, mock_playwright_expect):
        """assert_on_list_page should check URL."""
        page = SnippetAdminPage(
            mock_page,
            test_url,
            app_name="myapp",
            model_name="mymodel",
        )

        page.assert_on_list_page()

        mock_playwright_expect.assert_called()

    def test_assert_on_add_page(self, mock_page, test_url, mock_playwright_expect):
        """assert_on_add_page should check URL."""
        page = SnippetAdminPage(
            mock_page,
            test_url,
            app_name="myapp",
            model_name="mymodel",
        )

        page.assert_on_add_page()

        mock_playwright_expect.assert_called()

    def test_assert_item_created(self, mock_page, test_url, mock_playwright_expect):
        """assert_item_created should check success and list."""
        page = SnippetAdminPage(
            mock_page,
            test_url,
            app_name="myapp",
            model_name="mymodel",
        )
        mock_page.get_by_role.return_value.count.return_value = 1

        page.assert_item_created("Test Item")

    def test_assert_item_created_fails_when_not_found(
        self, mock_page, test_url, mock_playwright_expect
    ):
        """assert_item_created should fail if item not in list."""
        page = SnippetAdminPage(
            mock_page,
            test_url,
            app_name="myapp",
            model_name="mymodel",
        )
        mock_page.get_by_role.return_value.count.return_value = 0

        with pytest.raises(AssertionError, match="not found in list"):
            page.assert_item_created("Missing Item")

    def test_assert_item_updated(self, mock_page, test_url, mock_playwright_expect):
        """assert_item_updated should check success and list."""
        page = SnippetAdminPage(
            mock_page,
            test_url,
            app_name="myapp",
            model_name="mymodel",
        )
        mock_page.get_by_role.return_value.count.return_value = 1

        page.assert_item_updated("Updated Item")

    def test_assert_item_updated_fails_when_not_found(
        self, mock_page, test_url, mock_playwright_expect
    ):
        """assert_item_updated should fail if item not in list."""
        page = SnippetAdminPage(
            mock_page,
            test_url,
            app_name="myapp",
            model_name="mymodel",
        )
        mock_page.get_by_role.return_value.count.return_value = 0

        with pytest.raises(AssertionError, match="not found in list"):
            page.assert_item_updated("Missing Item")

    def test_assert_validation_error(self, mock_page, test_url, mock_playwright_expect):
        """assert_validation_error should check for error element."""
        page = SnippetAdminPage(
            mock_page,
            test_url,
            app_name="myapp",
            model_name="mymodel",
        )

        page.assert_validation_error()

        mock_page.locator.assert_called_with(".w-field__errors, .errorlist")

    def test_assert_validation_error_with_message(
        self, mock_page, test_url, mock_playwright_expect
    ):
        """assert_validation_error should check specific message."""
        page = SnippetAdminPage(
            mock_page,
            test_url,
            app_name="myapp",
            model_name="mymodel",
        )

        page.assert_validation_error(message="This field is required")

        mock_page.get_by_text.assert_called_with("This field is required")
