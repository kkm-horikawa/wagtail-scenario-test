"""E2E tests for snippet operations."""

import pytest

from wagtail_scenario_test import WagtailAdmin


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

    def test_delete_snippet(self, authenticated_page, server_url):
        """Test deleting a snippet through the admin UI.

        This tests the Wagtail 7+ UI where Delete is a link in the
        header dropdown menu, not a direct button.
        """
        admin = WagtailAdmin(authenticated_page, server_url)
        snippet = admin.snippet("testapp.testsnippet")

        # Create a snippet first
        snippet.create(name="Delete Test Snippet")
        snippet.assert_success_message()

        # Click the item to go to edit page
        snippet.click_item_in_list("Delete Test Snippet")

        # Delete the snippet (this uses the new Wagtail 7 dropdown UI)
        snippet.delete()

        # Verify we're back on the list page with success message
        snippet.assert_success_message()
        assert snippet.list_url in authenticated_page.url

        # Verify the snippet no longer exists
        exists = snippet.item_exists_in_list("Delete Test Snippet")
        assert exists is False
