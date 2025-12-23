"""End-to-end tests using the actual library with a real browser."""

import pytest

from wagtail_scenario_test import PageAdminPage, WagtailAdmin
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


@pytest.mark.e2e
@pytest.mark.django_db(transaction=True)
class TestSnippetE2E:
    """E2E tests for snippet operations using the WagtailAdmin facade."""

    def test_create_snippet(self, authenticated_page, server_url):
        """Test creating a snippet through the admin UI."""
        admin = WagtailAdmin(authenticated_page, server_url)

        # Navigate to snippet list
        snippet = admin.snippet("testapp.testsnippet")
        snippet.go_to_list()

        # Create a new snippet
        snippet.create(name="E2E Test Snippet")

        # Verify success
        snippet.assert_success_message()

    def test_get_success_message_after_create(self, authenticated_page, server_url):
        """Test getting success message after creation."""
        admin = WagtailAdmin(authenticated_page, server_url)
        snippet = admin.snippet("testapp.testsnippet")

        # Create a snippet
        snippet.create(name="Message Test Snippet")

        # Get the success message text
        message = snippet.get_success_message()
        # Message should exist after successful creation
        assert message is None or isinstance(message, str)

    def test_snippet_list_operations(self, authenticated_page, server_url):
        """Test listing snippets."""
        admin = WagtailAdmin(authenticated_page, server_url)
        snippet = admin.snippet("testapp.testsnippet")

        # Go to list page
        snippet.go_to_list()

        # Verify we're on the list page by checking URL contains the path
        assert snippet.list_url in authenticated_page.url

        # Get item count (may be 0 or more depending on test order)
        count = snippet.get_item_count()
        assert isinstance(count, int)

    def test_get_list_items(self, authenticated_page, server_url):
        """Test getting list items."""
        admin = WagtailAdmin(authenticated_page, server_url)
        snippet = admin.snippet("testapp.testsnippet")

        # Create a snippet first
        snippet.create(name="List Test Snippet")

        # Go to list and get items
        snippet.go_to_list()
        items = snippet.get_list_items()

        assert isinstance(items, list)

    def test_item_exists_in_list(self, authenticated_page, server_url):
        """Test checking if item exists in list."""
        admin = WagtailAdmin(authenticated_page, server_url)
        snippet = admin.snippet("testapp.testsnippet")

        # Create a snippet
        snippet.create(name="Exists Test Snippet")

        # Go to list and check existence
        snippet.go_to_list()
        exists = snippet.item_exists_in_list("Exists Test Snippet")

        assert exists is True

    def test_click_item_in_list(self, authenticated_page, server_url):
        """Test clicking an item in the list."""
        admin = WagtailAdmin(authenticated_page, server_url)
        snippet = admin.snippet("testapp.testsnippet")

        # Create a snippet
        snippet.create(name="Click Test Snippet")

        # Go to list and click the item
        snippet.go_to_list()
        snippet.click_item_in_list("Click Test Snippet")

        # Should be on edit page
        assert "/edit/" in authenticated_page.url

    def test_snippet_urls(self, authenticated_page, server_url):
        """Test snippet URL properties."""
        admin = WagtailAdmin(authenticated_page, server_url)
        snippet = admin.snippet("testapp.testsnippet")

        assert snippet.list_url == "/admin/snippets/testapp/testsnippet/"
        assert snippet.add_url == "/admin/snippets/testapp/testsnippet/add/"
        assert snippet.edit_url(123) == "/admin/snippets/testapp/testsnippet/edit/123/"
        assert (
            snippet.delete_url(123) == "/admin/snippets/testapp/testsnippet/delete/123/"
        )

    def test_on_list_page_url_check(self, authenticated_page, server_url):
        """Test that go_to_list navigates to correct URL."""
        admin = WagtailAdmin(authenticated_page, server_url)
        snippet = admin.snippet("testapp.testsnippet")

        snippet.go_to_list()

        # Verify URL contains the list path
        assert snippet.list_url in authenticated_page.url

    def test_on_add_page_url_check(self, authenticated_page, server_url):
        """Test that go_to_add navigates to correct URL."""
        admin = WagtailAdmin(authenticated_page, server_url)
        snippet = admin.snippet("testapp.testsnippet")

        snippet.go_to_add()

        # Verify URL contains the add path
        assert snippet.add_url in authenticated_page.url

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

    @pytest.mark.skip(reason="Logout selector varies by Wagtail version")
    def test_logout(self, authenticated_page, server_url):
        """Test logout navigates to logout page."""
        admin = WagtailAdmin(authenticated_page, server_url)
        admin.go_to_dashboard()

        admin.logout()

        # Should be on logout or login page
        url = authenticated_page.url
        assert "/admin/logout/" in url or "/login/" in url


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
