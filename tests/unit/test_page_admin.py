"""Unit tests for PageAdminPage."""

from wagtail_scenario_test.page_objects.wagtail_admin import PageAdminPage


class TestPageAdminPageNavigation:
    """Tests for PageAdminPage navigation methods."""

    def test_navigate_to_explorer(self, mock_page, test_url):
        """navigate_to_explorer should click Pages button and wait for panel."""
        page_admin = PageAdminPage(mock_page, test_url)

        page_admin.navigate_to_explorer()

        # Should click the Pages button
        mock_page.get_by_role.assert_called_once_with("button", name="Pages")
        mock_page.get_by_role.return_value.click.assert_called_once()

        # Should wait for the explorer panel
        mock_page.locator.assert_called_with(".c-page-explorer")
        mock_page.locator.return_value.wait_for.assert_called_once_with(
            state="visible", timeout=10000
        )

    def test_inherits_from_wagtail_admin_page(self, mock_page, test_url):
        """PageAdminPage should inherit from WagtailAdminPage."""
        page_admin = PageAdminPage(mock_page, test_url)

        # Should have access to WagtailAdminPage methods
        assert hasattr(page_admin, "login")
        assert hasattr(page_admin, "logout")
        assert hasattr(page_admin, "go_to_dashboard")
        assert hasattr(page_admin, "is_logged_in")
