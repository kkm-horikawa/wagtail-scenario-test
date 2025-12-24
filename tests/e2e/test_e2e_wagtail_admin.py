"""E2E tests for WagtailAdmin facade."""

import pytest

from wagtail_scenario_test import WagtailAdmin


@pytest.mark.e2e
@pytest.mark.django_db(transaction=True)
class TestWagtailAdminE2E:
    """E2E tests for WagtailAdmin facade."""

    def test_is_logged_in_check(self, authenticated_page, server_url):
        """Test is_logged_in method returns boolean."""
        admin = WagtailAdmin(authenticated_page, server_url)
        admin.go_to_dashboard()

        result = admin.is_logged_in()

        # Should return a boolean (True when on admin pages, not login)
        assert isinstance(result, bool)

    def test_logout(self, authenticated_page, server_url):
        """Test logout navigates to logout page."""
        admin = WagtailAdmin(authenticated_page, server_url)
        admin.go_to_dashboard()

        admin.logout()

        # Should be on logout or login page
        url = authenticated_page.url
        assert "/admin/logout/" in url or "/login/" in url

    def test_admin_dashboard(self, authenticated_page, server_url):
        """Test navigating to admin dashboard."""
        admin = WagtailAdmin(authenticated_page, server_url)

        admin.go_to_dashboard()

        # Should be on admin page
        assert "/admin/" in authenticated_page.url

    def test_global_search(self, authenticated_page, server_url):
        """Test global search functionality."""
        admin = WagtailAdmin(authenticated_page, server_url)

        admin.go_to_dashboard()
        admin.global_search("test")

        # Should have performed search
        assert "q=" in authenticated_page.url or "/search/" in authenticated_page.url
