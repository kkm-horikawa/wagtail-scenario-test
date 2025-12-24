"""Unit tests for WagtailAdmin facade."""

from wagtail_scenario_test.page_objects.facade import WagtailAdmin
from wagtail_scenario_test.page_objects.wagtail_admin import (
    PageAdminPage,
    SnippetAdminPage,
)


class TestWagtailAdminInit:
    """Tests for WagtailAdmin initialization."""

    def test_init_stores_page_and_base_url(self, mock_page, test_url):
        """WagtailAdmin should store page and base_url."""
        admin = WagtailAdmin(mock_page, test_url)

        assert admin.page is mock_page
        assert admin.base_url == test_url

    def test_init_strips_trailing_slash(self, mock_page):
        """WagtailAdmin should strip trailing slash from base_url."""
        admin = WagtailAdmin(mock_page, "http://localhost:8000/")

        assert admin.base_url == "http://localhost:8000"

    def test_init_creates_admin_page(self, mock_page, test_url):
        """WagtailAdmin should create internal WagtailAdminPage."""
        admin = WagtailAdmin(mock_page, test_url)

        assert admin._admin_page is not None
        assert admin._admin_page.page is mock_page


class TestWagtailAdminSnippet:
    """Tests for WagtailAdmin.snippet() method."""

    def test_snippet_with_full_format(self, mock_page, test_url):
        """snippet should parse app.model format."""
        admin = WagtailAdmin(mock_page, test_url)

        result = admin.snippet("myapp.mymodel")

        assert isinstance(result, SnippetAdminPage)
        assert result.app_name == "myapp"
        assert result.model_name == "mymodel"

    def test_snippet_with_short_format(self, mock_page, test_url):
        """snippet should use model as app_name for short format."""
        admin = WagtailAdmin(mock_page, test_url)

        result = admin.snippet("mymodel")

        assert isinstance(result, SnippetAdminPage)
        assert result.app_name == "mymodel"
        assert result.model_name == "mymodel"

    def test_snippet_with_multiple_dots(self, mock_page, test_url):
        """snippet should handle multiple dots in model name."""
        admin = WagtailAdmin(mock_page, test_url)

        result = admin.snippet("myapp.sub.model")

        assert result.app_name == "myapp"
        assert result.model_name == "sub.model"

    def test_snippet_returns_new_instance(self, mock_page, test_url):
        """snippet should return new instance each time."""
        admin = WagtailAdmin(mock_page, test_url)

        result1 = admin.snippet("myapp.mymodel")
        result2 = admin.snippet("myapp.mymodel")

        assert result1 is not result2

    def test_snippet_shares_page(self, mock_page, test_url):
        """snippet instances should share the same page."""
        admin = WagtailAdmin(mock_page, test_url)

        result = admin.snippet("myapp.mymodel")

        assert result.page is mock_page


class TestWagtailAdminDelegation:
    """Tests for WagtailAdmin delegated methods."""

    def test_go_to_dashboard(self, mock_page, test_url):
        """go_to_dashboard should delegate to admin page."""
        admin = WagtailAdmin(mock_page, test_url)

        admin.go_to_dashboard()

        mock_page.goto.assert_called_once_with(f"{test_url}/admin/")

    def test_search(self, mock_page, test_url):
        """search should delegate to admin page."""
        admin = WagtailAdmin(mock_page, test_url)

        admin.search("test query")

        mock_page.locator.assert_called_with("#id_q")

    def test_global_search(self, mock_page, test_url):
        """global_search should delegate to admin page."""
        admin = WagtailAdmin(mock_page, test_url)

        admin.global_search("my search")

        mock_page.get_by_placeholder.assert_called_with("Search")

    def test_logout(self, mock_page, test_url):
        """logout should delegate to admin page."""
        from unittest.mock import MagicMock

        # Setup mock for sidebar footer button
        mock_user_button = MagicMock()
        mock_user_button.count.return_value = 1
        mock_page.locator.return_value.first = mock_user_button

        # Setup mock for logout link
        mock_logout_link = MagicMock()
        mock_logout_link.count.return_value = 1
        mock_page.get_by_text.return_value = mock_logout_link

        admin = WagtailAdmin(mock_page, test_url)

        admin.logout()

        # Should click user button in sidebar footer
        mock_page.locator.assert_called_with(".sidebar-footer button")
        mock_user_button.click.assert_called_once()

        # Should click logout link
        mock_page.get_by_text.assert_called_with("Log out", exact=True)
        mock_logout_link.click.assert_called_once()

    def test_assert_success_message(self, mock_page, test_url, mock_playwright_expect):
        """assert_success_message should delegate to admin page."""
        admin = WagtailAdmin(mock_page, test_url)

        admin.assert_success_message()

        mock_page.locator.assert_called()

    def test_assert_success_message_with_contains(
        self, mock_page, test_url, mock_playwright_expect
    ):
        """assert_success_message should pass contains argument."""
        admin = WagtailAdmin(mock_page, test_url)

        admin.assert_success_message(contains="Created")

        mock_page.locator.assert_called()

    def test_assert_error_message(self, mock_page, test_url, mock_playwright_expect):
        """assert_error_message should delegate to admin page."""
        admin = WagtailAdmin(mock_page, test_url)

        admin.assert_error_message()

        mock_page.locator.assert_called_with(".w-message--error")

    def test_assert_error_message_with_contains(
        self, mock_page, test_url, mock_playwright_expect
    ):
        """assert_error_message should pass contains argument."""
        admin = WagtailAdmin(mock_page, test_url)

        admin.assert_error_message(contains="failed")

        mock_page.locator.assert_called()


class TestWagtailAdminChaining:
    """Tests for chained usage patterns."""

    def test_snippet_chaining(self, mock_page, test_url):
        """snippet methods should be chainable."""
        admin = WagtailAdmin(mock_page, test_url)

        # This should work without errors
        snippet = admin.snippet("myapp.mymodel")
        snippet.go_to_list()

        mock_page.goto.assert_called_with(f"{test_url}/admin/snippets/myapp/mymodel/")


class TestWagtailAdminAdditionalMethods:
    """Tests for additional WagtailAdmin methods."""

    def test_is_logged_in_returns_true_on_admin(self, mock_page, test_url):
        """is_logged_in should return True when on admin page."""
        mock_page.url = f"{test_url}/admin/"
        admin = WagtailAdmin(mock_page, test_url)

        result = admin.is_logged_in()

        assert result is True

    def test_is_logged_in_returns_false_on_login(self, mock_page, test_url):
        """is_logged_in should return False when on login page."""
        mock_page.url = f"{test_url}/admin/login/"
        admin = WagtailAdmin(mock_page, test_url)

        result = admin.is_logged_in()

        assert result is False

    def test_wait_for_navigation(self, mock_page, test_url):
        """wait_for_navigation should delegate to admin page."""
        admin = WagtailAdmin(mock_page, test_url)

        admin.wait_for_navigation()

        mock_page.wait_for_load_state.assert_called_once_with(
            "networkidle", timeout=30000
        )

    def test_wait_for_navigation_with_custom_timeout(self, mock_page, test_url):
        """wait_for_navigation should accept custom timeout."""
        admin = WagtailAdmin(mock_page, test_url)

        admin.wait_for_navigation(timeout=5000)

        mock_page.wait_for_load_state.assert_called_once_with(
            "networkidle", timeout=5000
        )


class TestWagtailAdminPages:
    """Tests for WagtailAdmin.pages() method."""

    def test_pages_returns_page_admin_page(self, mock_page, test_url):
        """pages() should return a PageAdminPage instance."""
        admin = WagtailAdmin(mock_page, test_url)

        result = admin.pages()

        assert isinstance(result, PageAdminPage)

    def test_pages_shares_page(self, mock_page, test_url):
        """pages() should share the same page instance."""
        admin = WagtailAdmin(mock_page, test_url)

        result = admin.pages()

        assert result.page is mock_page

    def test_pages_returns_new_instance(self, mock_page, test_url):
        """pages() should return new instance each time."""
        admin = WagtailAdmin(mock_page, test_url)

        result1 = admin.pages()
        result2 = admin.pages()

        assert result1 is not result2

    def test_pages_navigate_to_explorer(self, mock_page, test_url):
        """pages().navigate_to_explorer() should work."""
        admin = WagtailAdmin(mock_page, test_url)

        admin.pages().navigate_to_explorer()

        mock_page.get_by_role.assert_called_with("button", name="Pages")
