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
        """Log out of Wagtail admin by navigating to the logout URL."""
        self.goto(self.LOGOUT_URL)
        self.wait_for_navigation()

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

        In Wagtail 7+, the Delete action is a link in the header "More" dropdown
        menu, not a direct button. This method opens the dropdown and clicks
        the Delete link.

        Args:
            confirm: Whether to confirm the deletion
        """
        # In Wagtail 7+, Delete is in the header "More" dropdown as a link
        # Open the dropdown first using the w-dropdown controller
        dropdown_toggle = self.page.locator(
            "[data-controller='w-dropdown'] button[data-w-dropdown-target='toggle']"
        )
        dropdown_toggle.click()

        # Click the Delete link (not button) in the dropdown
        # Use exact=True to avoid matching items like "Delete Test Snippet"
        self.page.get_by_role("link", name="Delete", exact=True).click()

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


class PageAdminPage(WagtailAdminPage):
    """
    Page Object for Wagtail Page admin operations.

    Provides methods for interacting with pages in the Wagtail admin,
    including navigation through the page explorer.

    Example:
        page_admin = PageAdminPage(page, base_url)
        page_admin.login("admin", "password")
        page_admin.navigate_to_explorer()
    """

    # =========================================================================
    # Navigation
    # =========================================================================

    def navigate_to_explorer(self) -> None:
        """
        Navigate to the page explorer.

        Opens the page explorer panel by clicking the "Pages" button
        in the sidebar. The explorer panel allows browsing and managing
        the page tree.
        """
        self.page.get_by_role("button", name="Pages").click()
        # Wait for the explorer panel to open (uses role="dialog" and aria-label)
        self.page.locator(".c-page-explorer").wait_for(state="visible", timeout=10000)

    # =========================================================================
    # URLs
    # =========================================================================

    def add_child_page_url(
        self, parent_page_id: int, app_name: str, model_name: str
    ) -> str:
        """
        Return the URL for adding a child page.

        Args:
            parent_page_id: Parent page ID
            app_name: Django app name (e.g., "testapp")
            model_name: Model name in lowercase (e.g., "testpage")
        """
        return f"/admin/pages/add/{app_name}/{model_name}/{parent_page_id}/"

    def edit_page_url(self, page_id: int) -> str:
        """
        Return the URL for editing a page.

        Args:
            page_id: The page ID to edit
        """
        return f"/admin/pages/{page_id}/edit/"

    def delete_page_url(self, page_id: int) -> str:
        """
        Return the URL for deleting a page.

        Args:
            page_id: The page ID to delete
        """
        return f"/admin/pages/{page_id}/delete/"

    # =========================================================================
    # Page Navigation
    # =========================================================================

    def edit_page(self, page_id: int) -> None:
        """
        Navigate to the edit page for an existing page.

        Args:
            page_id: The page ID to edit

        Example:
            page_admin.edit_page(5)  # Navigate to edit page with ID 5
        """
        self.goto(self.edit_page_url(page_id))
        self.wait_for_navigation()

    # =========================================================================
    # Page Deletion
    # =========================================================================

    def delete_page(self, page_id: int, confirm: bool = True) -> None:
        """
        Delete a page.

        In Wagtail 7+, the Delete action is a link in the "Actions" dropdown
        menu on the edit page. This method navigates to the edit page, opens
        the dropdown, and clicks the Delete link.

        Args:
            page_id: The page ID to delete
            confirm: Whether to confirm the deletion (default True)

        Example:
            page_admin.delete_page(5)  # Delete page with ID 5
            page_admin.delete_page(5, confirm=False)  # Go to confirm page only
        """
        # Navigate to the edit page first (delete is in edit page dropdown)
        self.edit_page(page_id)

        # Open the "Actions" dropdown which contains Delete, Copy, Move, etc.
        # This is labeled "Actions" with an aria-label, and shows as "… Actions"
        # Use exact=True to avoid matching "More actions" button
        dropdown_toggle = self.page.get_by_role("button", name="Actions", exact=True)
        dropdown_toggle.click()

        # Click the Delete link (not button) in the dropdown
        # Use exact=True to avoid matching items like "Delete Test Page"
        self.page.get_by_role("link", name="Delete", exact=True).click()

        if confirm:
            self.page.get_by_role("button", name="Yes, delete").click()
        self.wait_for_navigation()

    # =========================================================================
    # Page Publishing
    # =========================================================================

    def publish(self, page_id: int | None = None) -> None:
        """
        Publish a page.

        If page_id is provided, navigates to the edit page first.
        Otherwise, assumes we are already on the page edit screen.

        In Wagtail, the Publish button is in a dropdown menu at the bottom
        of the page editor. This method opens the dropdown and clicks Publish.

        Args:
            page_id: Optional page ID to publish. If provided, navigates to
                the edit page first. If None, assumes already on edit page.

        Example:
            # Publish a specific page by ID
            page_admin.publish(page_id=5)

            # Or navigate to edit page first, then publish
            page_admin.edit_page(5)
            # ... make some edits ...
            page_admin.publish()
        """
        if page_id is not None:
            self.edit_page(page_id)

        # Publish is in the "More actions" dropdown menu at the bottom of the editor
        # This dropdown contains Save draft, Publish, and other save-related actions
        # Note: The "Actions" dropdown (at the top) contains Delete, Copy, Move
        self.page.get_by_role("button", name="More actions").click()
        self.page.get_by_role("button", name="Publish").click()
        self.wait_for_navigation()

    def unpublish(self, page_id: int | None = None, confirm: bool = True) -> None:
        """
        Unpublish a live page.

        If page_id is provided, navigates to the edit page first.
        Otherwise, assumes we are already on the page edit screen.

        In Wagtail, the Unpublish action is in the "Actions" dropdown menu
        at the top of the page editor (same dropdown as Delete, Copy, Move).

        Args:
            page_id: Optional page ID to unpublish. If provided, navigates to
                the edit page first. If None, assumes already on edit page.
            confirm: Whether to confirm the unpublish action (default True)

        Example:
            # Unpublish a specific page by ID
            page_admin.unpublish(page_id=5)

            # Or navigate to edit page first, then unpublish
            page_admin.edit_page(5)
            page_admin.unpublish()

            # Go to confirmation page without confirming
            page_admin.unpublish(page_id=5, confirm=False)
        """
        if page_id is not None:
            self.edit_page(page_id)

        # Unpublish is in the "Actions" dropdown (same as Delete, Copy, Move)
        # This is different from the "More actions" dropdown which has Publish
        self.page.get_by_role("button", name="Actions", exact=True).click()

        # Click the Unpublish link in the dropdown
        self.page.get_by_role("link", name="Unpublish", exact=True).click()

        if confirm:
            self.page.get_by_role("button", name="Yes, unpublish").click()
        self.wait_for_navigation()

    # =========================================================================
    # Page Creation
    # =========================================================================

    def create_child_page(
        self,
        parent_page_id: int,
        page_type: str,
        *,
        title: str,
        slug: str | None = None,
        save: bool = True,
        publish: bool = False,
        **fields: str,
    ) -> None:
        """
        Create a child page under a parent.

        Navigates directly to the page creation form and fills in the
        specified fields.

        Args:
            parent_page_id: Parent page ID
            page_type: Page type in "app_name.ModelName" format
                (e.g., "testapp.TestPage")
            title: Page title (required by Wagtail)
            slug: Page slug (required by Wagtail). If not provided,
                a slug will be generated from the title.
            save: Whether to save the page (default True)
            publish: Whether to publish instead of saving as draft
                (only applies if save=True)
            **fields: Additional fields to fill (field_id=value).
                Field IDs should be without the "#" prefix.

        Example:
            # Create a simple page as draft
            page_admin.create_child_page(
                parent_page_id=1,
                page_type="testapp.TestPage",
                title="My New Page",
                slug="my-new-page",
            )

            # Create and publish with additional fields
            page_admin.create_child_page(
                parent_page_id=1,
                page_type="testapp.TestPage",
                title="My Published Page",
                slug="my-published-page",
                publish=True,
                id_subtitle="A subtitle",
                id_body="Page body content",
            )
        """
        # Parse page_type to get app_name and model_name
        app_name, model_name = page_type.split(".")
        model_name = model_name.lower()

        # Navigate to the add page form
        url = self.add_child_page_url(parent_page_id, app_name, model_name)
        self.goto(url)
        self.wait_for_navigation()

        # Fill the title field (required)
        title_input = self.page.locator("#id_title")
        title_input.wait_for(state="visible", timeout=10000)
        title_input.fill(title)

        # Fill additional fields in Content tab
        for field_id, value in fields.items():
            selector = field_id if field_id.startswith("#") else f"#{field_id}"
            self.page.locator(selector).fill(value)

        # Fill slug in Promote tab (required by Wagtail)
        actual_slug = slug if slug else self._generate_slug(title)
        self.page.get_by_role("tab", name="Promote").click()
        slug_input = self.page.locator("#id_slug")
        slug_input.wait_for(state="visible", timeout=10000)
        slug_input.fill(actual_slug)

        if save:
            if publish:
                # Publish is in a dropdown menu - expand it first
                dropdown_toggle = (
                    "[data-controller='w-dropdown'] "
                    "button[data-w-dropdown-target='toggle']"
                )
                self.page.locator(dropdown_toggle).click()
                self.page.get_by_role("button", name="Publish").click()
            else:
                self.page.get_by_role("button", name="Save draft").click()
            self.wait_for_navigation()

    def _generate_slug(self, title: str) -> str:
        """
        Generate a slug from a title.

        Args:
            title: Page title

        Returns:
            URL-friendly slug
        """
        import re

        slug = title.lower()
        slug = re.sub(r"[^\w\s-]", "", slug)
        slug = re.sub(r"[\s_]+", "-", slug)
        slug = re.sub(r"-+", "-", slug)
        return slug.strip("-")
