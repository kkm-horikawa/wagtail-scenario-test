"""E2E tests for BasePage base class functionality."""

import pytest

from wagtail_scenario_test.page_objects import BasePage


@pytest.mark.e2e
@pytest.mark.django_db(transaction=True)
class TestBasePageE2E:
    """E2E tests for BasePage base class functionality."""

    def test_goto_navigates_to_path(self, authenticated_page, server_url):
        """Test goto method navigates correctly."""
        base = BasePage(authenticated_page, server_url)

        base.goto("/admin/")

        assert "/admin/" in authenticated_page.url

    def test_current_path_returns_path(self, authenticated_page, server_url):
        """Test current_path returns URL path."""
        base = BasePage(authenticated_page, server_url)
        authenticated_page.goto(f"{server_url}/admin/")

        path = base.current_path()

        assert path == "/admin/"

    def test_reload_reloads_page(self, authenticated_page, server_url):
        """Test reload method works."""
        base = BasePage(authenticated_page, server_url)
        authenticated_page.goto(f"{server_url}/admin/")

        base.reload()

        assert "/admin/" in authenticated_page.url

    def test_wait_for_navigation(self, authenticated_page, server_url):
        """Test wait_for_navigation waits for page load."""
        base = BasePage(authenticated_page, server_url)
        authenticated_page.goto(f"{server_url}/admin/")

        # Should not raise
        base.wait_for_navigation()

    def test_wait_for_element(self, authenticated_page, server_url):
        """Test wait_for_element waits for selector."""
        base = BasePage(authenticated_page, server_url)
        authenticated_page.goto(f"{server_url}/admin/")

        # Wait for body element (always exists)
        element = base.wait_for_element("body")
        assert element is not None

    def test_assert_visible(self, authenticated_page, server_url):
        """Test assert_visible checks text visibility."""
        base = BasePage(authenticated_page, server_url)
        authenticated_page.goto(f"{server_url}/admin/")

        # Assert that "Snippets" text is visible (always in sidebar)
        base.assert_visible("Snippets")

    def test_get_page_content(self, authenticated_page, server_url):
        """Test get_page_content returns HTML."""
        base = BasePage(authenticated_page, server_url)
        authenticated_page.goto(f"{server_url}/admin/")

        content = base.get_page_content()

        assert "<html" in content.lower()
        assert "</html>" in content.lower()

    def test_get_visible_text(self, authenticated_page, server_url):
        """Test get_visible_text returns body text."""
        base = BasePage(authenticated_page, server_url)
        authenticated_page.goto(f"{server_url}/admin/")

        text = base.get_visible_text()

        assert isinstance(text, str)
        assert len(text) > 0
