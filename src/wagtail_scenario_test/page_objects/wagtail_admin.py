"""
Page Objects for Wagtail Admin interface.

These classes provide high-level abstractions for interacting with
Wagtail's admin interface in E2E tests.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from playwright.sync_api import expect

from wagtail_scenario_test.page_objects.base import BasePage

if TYPE_CHECKING:
    from playwright.sync_api import Page


class WagtailAdminPage(BasePage):
    """
    Page Object for general Wagtail Admin operations.

    Provides methods for common admin tasks like navigation,
    searching, and accessing different sections.

    Example:
        admin = WagtailAdminPage(page, base_url)
        admin.login("admin", "password")
        admin.go_to_dashboard()
    """

    # =========================================================================
    # URLs
    # =========================================================================

    ADMIN_ROOT = "/admin/"
    LOGIN_URL = "/admin/login/"
    LOGOUT_URL = "/admin/logout/"

    # =========================================================================
    # Authentication
    # =========================================================================

    def login(self, username: str, password: str) -> None:
        """
        Log into Wagtail admin.

        Args:
            username: Admin username
            password: Admin password
        """
        self.goto(self.LOGIN_URL)
        self.page.get_by_label("Username").fill(username)
        self.page.get_by_label("Password").fill(password)
        self.page.get_by_role("button", name="Sign in").click()
        self.page.wait_for_url(f"**{self.ADMIN_ROOT}**")

    def logout(self) -> None:
        """Log out of Wagtail admin."""
        self.goto(self.LOGOUT_URL)

    def is_logged_in(self) -> bool:
        """Check if currently logged in."""
        return self.LOGIN_URL not in self.page.url

    # =========================================================================
    # Navigation
    # =========================================================================

    def go_to_dashboard(self) -> None:
        """Navigate to admin dashboard."""
        self.goto(self.ADMIN_ROOT)

    def open_sidebar_menu(self, menu_name: str) -> None:
        """
        Open a sidebar menu item.

        Args:
            menu_name: Menu button text
        """
        self.page.get_by_role("button", name=menu_name).click()

    def click_sidebar_link(self, link_name: str) -> None:
        """
        Click a link in the sidebar.

        Args:
            link_name: Link text
        """
        self.page.get_by_role("link", name=link_name).click()

    # =========================================================================
    # Search
    # =========================================================================

    def search(self, query: str) -> None:
        """
        Perform a search in the admin list view.

        Args:
            query: Search query
        """
        search_input = self.page.locator("#id_q")
        search_input.fill(query)
        search_input.press("Enter")
        self.wait_for_navigation()

    def global_search(self, query: str) -> None:
        """
        Perform a global search using the sidebar search.

        Args:
            query: Search query
        """
        self.page.get_by_placeholder("Search").first.fill(query)
        self.page.get_by_placeholder("Search").first.press("Enter")
        self.wait_for_navigation()

    # =========================================================================
    # Notifications
    # =========================================================================

    def get_success_message(self) -> str | None:
        """
        Get the text of a success notification if present.

        Returns:
            Success message text or None
        """
        success = self.page.locator(".w-message--success")
        if success.count() > 0:
            return success.first.text_content()
        return None

    def get_error_message(self) -> str | None:
        """
        Get the text of an error notification if present.

        Returns:
            Error message text or None
        """
        error = self.page.locator(".w-message--error")
        if error.count() > 0:
            return error.first.text_content()
        return None

    def assert_success_message(self, contains: str | None = None) -> None:
        """
        Assert a success message is displayed.

        Args:
            contains: Optional text that should be in the message
        """
        # Multiple selectors for Wagtail version compatibility
        success = self.page.locator(
            ".w-message--success, .success, "
            "[data-w-messages-target='container'] .success"
        )
        expect(success.first).to_be_visible(timeout=10000)
        if contains:
            expect(success.first).to_contain_text(contains)

    def assert_error_message(self, contains: str | None = None) -> None:
        """
        Assert an error message is displayed.

        Args:
            contains: Optional text that should be in the message
        """
        error = self.page.locator(".w-message--error")
        expect(error).to_be_visible()
        if contains:
            expect(error).to_contain_text(contains)


class SnippetAdminPage(WagtailAdminPage):
    """
    Page Object for Wagtail Snippet admin operations.

    This is a generic class that can be used for any Wagtail snippet
    by specifying the app_name and model_name.

    Example:
        # For a ReusableBlock snippet in wagtail_reusable_blocks app
        page = SnippetAdminPage(
            browser_page,
            base_url,
            app_name="wagtail_reusable_blocks",
            model_name="reusableblock"
        )
        page.create(name="My Block")

        # For a custom snippet
        page = SnippetAdminPage(
            browser_page,
            base_url,
            app_name="myapp",
            model_name="mysnippet"
        )
    """

    def __init__(
        self,
        page: Page,
        base_url: str,
        *,
        app_name: str,
        model_name: str,
    ) -> None:
        """
        Initialize the Snippet Admin Page Object.

        Args:
            page: Playwright Page instance
            base_url: Base URL of the test server
            app_name: Django app name (e.g., "wagtail_reusable_blocks")
            model_name: Model name in lowercase (e.g., "reusableblock")
        """
        super().__init__(page, base_url)
        self.app_name = app_name
        self.model_name = model_name

    # =========================================================================
    # URLs
    # =========================================================================

    @property
    def list_url(self) -> str:
        """Return the snippet list URL."""
        return f"/admin/snippets/{self.app_name}/{self.model_name}/"

    @property
    def add_url(self) -> str:
        """Return the snippet add URL."""
        return f"/admin/snippets/{self.app_name}/{self.model_name}/add/"

    def edit_url(self, item_id: int) -> str:
        """
        Return the edit URL for a snippet.

        Args:
            item_id: Snippet primary key
        """
        return f"/admin/snippets/{self.app_name}/{self.model_name}/edit/{item_id}/"

    def delete_url(self, item_id: int) -> str:
        """
        Return the delete URL for a snippet.

        Args:
            item_id: Snippet primary key
        """
        return f"/admin/snippets/{self.app_name}/{self.model_name}/delete/{item_id}/"

    # =========================================================================
    # Navigation
    # =========================================================================

    def go_to_list(self) -> None:
        """Navigate to the snippet list page."""
        self.goto(self.list_url)

    def go_to_add(self) -> None:
        """Navigate to the add snippet page."""
        self.goto(self.add_url)

    def go_to_edit(self, item_id: int) -> None:
        """
        Navigate to edit a specific snippet.

        Args:
            item_id: Snippet primary key
        """
        self.goto(self.edit_url(item_id))

    # =========================================================================
    # Create operations
    # =========================================================================

    def create(
        self,
        *,
        name: str | None = None,
        save: bool = True,
        **fields: str,
    ) -> None:
        """
        Create a new snippet.

        Args:
            name: Value for the name field (if the snippet has one)
            save: Whether to save after filling the form
            **fields: Additional fields to fill (field_id=value)

        Example:
            # Simple creation with just name
            page.create(name="My Item")

            # With additional fields
            page.create(name="My Item", id_slug="my-slug", id_description="...")
        """
        self.go_to_add()
        self.wait_for_navigation()

        # Fill name field if provided
        if name is not None:
            name_input = self.page.locator("#id_name")
            name_input.wait_for(state="visible", timeout=10000)
            name_input.fill(name)

        # Fill additional fields
        for field_id, value in fields.items():
            # Ensure field_id has # prefix
            selector = field_id if field_id.startswith("#") else f"#{field_id}"
            self.page.locator(selector).fill(value)

        if save:
            self.save()

    # =========================================================================
    # Form interactions
    # =========================================================================

    def save(self) -> None:
        """Click the Save button."""
        self.page.get_by_role("button", name="Save").click()
        self.wait_for_navigation()

    def save_draft(self) -> None:
        """Save as draft (if available)."""
        self.page.get_by_role("button", name="Save draft").click()
        self.wait_for_navigation()

    def delete(self, confirm: bool = True) -> None:
        """
        Delete the current snippet.

        Args:
            confirm: Whether to confirm the deletion
        """
        self.page.get_by_role("button", name="Delete").click()
        if confirm:
            self.page.get_by_role("button", name="Yes, delete").click()
        self.wait_for_navigation()

    # =========================================================================
    # List operations
    # =========================================================================

    def get_item_count(self) -> int:
        """
        Return the number of items in the list.

        Returns:
            Number of items
        """
        self.go_to_list()
        rows = self.page.locator("table tbody tr")
        return rows.count()

    def item_exists_in_list(self, title: str) -> bool:
        """
        Check if an item with the given title exists in the list.

        Args:
            title: Item title to look for

        Returns:
            True if found, False otherwise
        """
        self.go_to_list()
        return self.page.get_by_role("link", name=title).count() > 0

    def click_item_in_list(self, title: str) -> None:
        """
        Click on an item in the list to edit it.

        Args:
            title: Item title to click
        """
        self.go_to_list()
        self.page.get_by_role("link", name=title).click()
        self.wait_for_navigation()

    def get_list_items(self) -> list[str]:
        """
        Get all item titles from the list.

        Returns:
            List of item titles
        """
        self.go_to_list()
        links = self.page.locator("table tbody tr td a").all()
        return [link.text_content() or "" for link in links]

    # =========================================================================
    # Assertions
    # =========================================================================

    def assert_on_list_page(self) -> None:
        """Assert we're on the snippet list page."""
        self.assert_url_contains(self.list_url)

    def assert_on_add_page(self) -> None:
        """Assert we're on the add snippet page."""
        self.assert_url_contains(self.add_url)

    def assert_item_created(self, title: str) -> None:
        """
        Assert an item was successfully created.

        Args:
            title: Expected item title
        """
        self.assert_success_message()
        assert self.item_exists_in_list(title), f"Item '{title}' not found in list"

    def assert_item_updated(self, title: str) -> None:
        """
        Assert an item was successfully updated.

        Args:
            title: Expected item title
        """
        self.assert_success_message()
        assert self.item_exists_in_list(title), f"Item '{title}' not found in list"

    def assert_validation_error(self, message: str | None = None) -> None:
        """
        Assert a validation error is displayed.

        Args:
            message: Optional specific error message to check for
        """
        error = self.page.locator(".w-field__errors, .errorlist")
        expect(error.first).to_be_visible(timeout=5000)
        if message:
            self.assert_visible(message)
