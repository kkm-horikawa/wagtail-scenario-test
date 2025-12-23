"""E2E tests for PageAdminPage."""

import pytest

from wagtail_scenario_test import PageAdminPage


@pytest.mark.e2e
@pytest.mark.django_db(transaction=True)
class TestPageAdminE2E:
    """E2E tests for PageAdminPage."""

    def test_navigate_to_explorer(self, authenticated_page, server_url):
        """Test navigating to the page explorer."""
        page_admin = PageAdminPage(authenticated_page, server_url)
        page_admin.go_to_dashboard()

        page_admin.navigate_to_explorer()

        # The explorer panel should be visible
        explorer = authenticated_page.locator(".c-page-explorer")
        assert explorer.is_visible()
