"""
WagtailAdmin Facade - Simplified API for Wagtail E2E testing.

This module provides a facade class that wraps Page Objects and provides
a simpler, more intuitive API for common operations.

Example:
    admin = WagtailAdmin(page, base_url)
    admin.snippet("myapp.mymodel").create(name="Test")
    admin.snippet("myapp.mymodel").assert_item_created("Test")
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from wagtail_scenario_test.page_objects.wagtail_admin import (
    SnippetAdminPage,
    WagtailAdminPage,
)

if TYPE_CHECKING:
    from playwright.sync_api import Page


class WagtailAdmin:
    """
    Facade class for Wagtail admin operations.

    Provides a unified, simplified API for interacting with Wagtail admin.
    This class wraps the underlying Page Objects and provides convenient
    factory methods.

    Example:
        # Basic usage
        admin = WagtailAdmin(page, base_url)

        # Work with snippets
        snippet = admin.snippet("myapp.mymodel")
        snippet.create(name="New Item")
        snippet.assert_success_message()

        # Direct admin operations
        admin.search("query")
        admin.go_to_dashboard()

    Attributes:
        page: The Playwright Page instance
        base_url: The base URL of the Wagtail site
    """

    def __init__(self, page: Page, base_url: str) -> None:
        """
        Initialize the WagtailAdmin facade.

        Args:
            page: Playwright Page instance (usually from authenticated_page fixture)
            base_url: Base URL of the test server (usually from server_url fixture)
        """
        self.page = page
        self.base_url = base_url.rstrip("/")
        self._admin_page = WagtailAdminPage(page, base_url)

    # =========================================================================
    # Factory methods for Page Objects
    # =========================================================================

    def snippet(self, model: str) -> SnippetAdminPage:
        """
        Get a SnippetAdminPage for the specified model.

        Args:
            model: Model identifier in "app_name.model_name" or "model_name" format.
                   If only model_name is provided, app_name defaults to model_name.

        Returns:
            SnippetAdminPage configured for the specified model

        Example:
            # Full format
            admin.snippet("wagtail_reusable_blocks.reusableblock")

            # Short format (app_name = model_name)
            admin.snippet("mymodel")
        """
        if "." in model:
            app_name, model_name = model.split(".", 1)
        else:
            # Default: assume app_name matches model_name
            app_name = model
            model_name = model

        return SnippetAdminPage(
            self.page,
            self.base_url,
            app_name=app_name,
            model_name=model_name,
        )

    # =========================================================================
    # Delegate common admin operations
    # =========================================================================

    def go_to_dashboard(self) -> None:
        """Navigate to admin dashboard."""
        self._admin_page.go_to_dashboard()

    def search(self, query: str) -> None:
        """
        Perform a search in the admin.

        Args:
            query: Search query
        """
        self._admin_page.search(query)

    def global_search(self, query: str) -> None:
        """
        Perform a global search using the sidebar search.

        Args:
            query: Search query
        """
        self._admin_page.global_search(query)

    def logout(self) -> None:
        """Log out of Wagtail admin."""
        self._admin_page.logout()

    def is_logged_in(self) -> bool:
        """
        Check if currently logged into admin.

        Returns:
            True if on admin page (not login page)
        """
        return self._admin_page.is_logged_in()

    def wait_for_navigation(self, timeout: int = 30000) -> None:
        """
        Wait for page navigation to complete.

        Args:
            timeout: Maximum wait time in milliseconds
        """
        self._admin_page.wait_for_navigation(timeout)

    def assert_success_message(self, contains: str | None = None) -> None:
        """
        Assert a success message is displayed.

        Args:
            contains: Optional text that should be in the message
        """
        self._admin_page.assert_success_message(contains)

    def assert_error_message(self, contains: str | None = None) -> None:
        """
        Assert an error message is displayed.

        Args:
            contains: Optional text that should be in the message
        """
        self._admin_page.assert_error_message(contains)
