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

    def preview_url(self, page_id: int) -> str:
        """
        Return the preview URL for a page.

        This returns the URL for viewing a page preview within the Wagtail admin.
        The preview is displayed in an iframe on the edit page.

        Args:
            page_id: The page ID to preview
        """
        return f"/admin/pages/{page_id}/edit/preview/"

    def get_live_url(self) -> str | None:
        """
        Get the live URL of the current page from the editor.

        Must be on a page edit screen. Returns the href of the status link,
        or None if the page is not published or has no routable URL.

        In Wagtail 7+, published pages show a status link (with aria-label
        containing "Visit the live page") that links to the live URL.

        Returns:
            The live URL of the page, or None if not available.

        Example:
            page_admin.edit_page(5)
            url = page_admin.get_live_url()
            # Returns something like "/my-page/" or None if not published
        """
        # In Wagtail 7+, the status link has aria-label "Visit the live page"
        # This is more specific than just "Live" which can match multiple elements
        link = self.page.locator("a.page-status-tag[href]")
        if link.count() == 0:
            return None
        return link.first.get_attribute("href")

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

    def visit_preview(self, page_id: int) -> None:
        """
        Navigate to the preview of a page.

        This opens the page preview in the browser. The preview shows
        the page as it would appear on the frontend, including any
        unsaved changes in the editor.

        Args:
            page_id: The page ID to preview

        Example:
            page_admin.visit_preview(5)  # Preview page with ID 5
        """
        self.goto(self.preview_url(page_id))
        self.wait_for_navigation()

    def visit_live(self, page_id: int) -> None:
        """
        Navigate to the live URL of a published page.

        This first navigates to the edit page to get the live URL,
        then navigates to that URL. Requires the page to be published.

        Args:
            page_id: The page ID to view live

        Raises:
            ValueError: If the page is not published or has no live URL

        Example:
            page_admin.visit_live(5)  # View live page with ID 5
        """
        self.edit_page(page_id)
        live_url = self.get_live_url()
        if live_url is None:
            raise ValueError(f"Page {page_id} is not published or has no routable URL")
        self.goto(live_url)
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


class BlockPath:
    """
    Fluent builder for navigating StreamField block structures.

    BlockPath allows chaining methods to navigate into nested block structures
    (StructBlocks, ListBlocks) and perform actions like fill() or value().

    This class is not instantiated directly - use StreamFieldHelper.block() instead.

    Example:
        sf = StreamFieldHelper(page, "body")

        # Simple block
        sf.block(0).fill("Hello")

        # StructBlock
        sf.block(0).struct("title").fill("Welcome")

        # ListBlock > StructBlock
        sf.block(0).item(0).struct("title").fill("Card Title")

        # Deep nesting
        sf.block(0).item(0).struct("cards").item(0).struct("name").fill("Name")
    """

    def __init__(self, helper: StreamFieldHelper, path_id: str) -> None:
        """
        Initialize BlockPath.

        Args:
            helper: The parent StreamFieldHelper instance
            path_id: Current path ID (e.g., "body-0" or "body-0-value-title")
        """
        self._helper = helper
        self._id = path_id

    def struct(self, field_name: str) -> BlockPath:
        """
        Navigate into a StructBlock field.

        Args:
            field_name: The name of the field within the StructBlock

        Returns:
            BlockPath: A new BlockPath pointing to the struct field

        Example:
            sf.block(0).struct("title").fill("Welcome")
            sf.block(0).struct("hero").struct("subtitle").fill("Sub")
        """
        # If we're at a -value path (after item()), just add field name
        # Otherwise, add -value- prefix
        if self._id.endswith("-value"):
            return BlockPath(self._helper, f"{self._id}-{field_name}")
        else:
            return BlockPath(self._helper, f"{self._id}-value-{field_name}")

    def item(self, index: int) -> BlockPath:
        """
        Navigate into a ListBlock item.

        Args:
            index: The index of the item within the ListBlock (0-based)

        Returns:
            BlockPath: A new BlockPath pointing to the list item

        Example:
            sf.block(0).item(0).fill("First item")
            sf.block(0).item(0).struct("title").fill("Card Title")
        """
        # If the path ends with digit or -value, we're at block level or item level
        # Add full list item path: -value-{index}-value
        # If the path ends with a field name (from struct()), just add -{index}-value
        last_segment = self._id.split("-")[-1]
        if last_segment.isdigit() or self._id.endswith("-value"):
            return BlockPath(self._helper, f"{self._id}-value-{index}-value")
        else:
            return BlockPath(self._helper, f"{self._id}-{index}-value")

    def fill(self, value: str) -> None:
        """
        Fill the current field with a value.

        Works for CharBlock, TextBlock, URLBlock, and other simple input fields.

        Args:
            value: The value to fill

        Example:
            sf.block(0).fill("Simple block value")
            sf.block(0).struct("title").fill("Struct field value")
        """
        selector = self._build_value_selector()
        field = self._helper.page.locator(selector)

        if field.count() > 0:
            field.fill(value)
        else:
            # Try textarea for TextBlock, etc.
            name = selector[1:]  # Remove # prefix to get name
            textarea = self._helper.page.locator(f"textarea[name='{name}']")
            if textarea.count() > 0:
                textarea.fill(value)

    def value(self) -> str:
        """
        Get the current value of the field.

        Returns:
            str: The current value, or empty string if not found

        Example:
            title = sf.block(0).struct("title").value()
        """
        selector = self._build_value_selector()
        field = self._helper.page.locator(selector)
        if field.count() > 0:
            return field.input_value()

        # Try textarea for TextBlock, etc.
        name = selector[1:]  # Remove # prefix to get name
        textarea = self._helper.page.locator(f"textarea[name='{name}']")
        if textarea.count() > 0:
            return textarea.input_value()

        return ""

    def click_chooser(self) -> None:
        """
        Click the chooser button (for ImageChooserBlock, DocumentChooserBlock, etc.).

        Opens the chooser modal for selecting an image, document, or other media.

        Example:
            sf.block(0).click_chooser()  # Standalone chooser
            sf.block(0).struct("image").click_chooser()  # Chooser in StructBlock
        """
        container_id = self._id if "-value" in self._id else f"{self._id}-value"

        chooser_button = self._helper.page.locator(
            f"[id^='{container_id}'] .chooser__choose-button, "
            f"#panel-child-content-{container_id}-section .chooser__choose-button"
        ).first

        if chooser_button.count() > 0:
            chooser_button.click()
            self._helper.page.wait_for_timeout(500)

    def add_item(self) -> int:
        """
        Add a new item to a ListBlock at this path.

        Returns:
            int: The index of the newly added item

        Example:
            new_index = sf.block(0).add_item()
            sf.block(0).item(new_index).struct("title").fill("New Card")
        """
        # Determine the count input name
        if "-value" in self._id:
            count_name = f"{self._id}-count"
        else:
            count_name = f"{self._id}-value-count"

        # Get current item count
        count_input = self._helper.page.locator(f"input[name='{count_name}']")
        current_count = 0
        if count_input.count() > 0:
            val = count_input.input_value()
            current_count = int(val) if val else 0

        path_parts = self._id.split("-")

        # Check if we're at a struct field level (e.g., body-0-value-cards)
        # vs block level (e.g., body-0)
        if "-value-" in self._id and not path_parts[-1].isdigit():
            # Struct field level - use data-contentpath
            field_name = path_parts[-1]
            container = self._helper.page.locator(f"[data-contentpath='{field_name}']")
            add_button = container.locator(".c-sf-add-button").last
        else:
            # Block level - find the block's panel by getting the panel ID
            # from the count input's ancestor, then find add button inside
            if count_input.count() > 0:
                # Get the panel ID from JavaScript
                panel_id = count_input.evaluate("""el => {
                    let current = el;
                    while (current) {
                        current = current.parentElement;
                        if (current && current.classList.contains('w-panel')) {
                            return current.id;
                        }
                    }
                    return null;
                }""")
                if panel_id:
                    container = self._helper.page.locator(f"#{panel_id}")
                    add_button = container.locator(".c-sf-add-button").last
                else:
                    add_button = self._helper.page.locator("nonexistent")
            else:
                add_button = self._helper.page.locator("nonexistent")

        if add_button.count() > 0:
            add_button.click()
            self._helper.page.wait_for_timeout(300)

        return current_count

    def item_count(self) -> int:
        """
        Get the number of items in a ListBlock at this path.

        Returns:
            int: The number of items in the ListBlock

        Example:
            count = sf.block(0).item_count()
        """
        if "-value" in self._id:
            count_name = f"{self._id}-count"
        else:
            count_name = f"{self._id}-value-count"
        count_input = self._helper.page.locator(f"input[name='{count_name}']")
        if count_input.count() > 0:
            val = count_input.input_value()
            return int(val) if val else 0
        return 0

    def _build_value_selector(self) -> str:
        """Build the CSS selector for the value input."""
        # If we're at block level (ends with digit, no -value yet), add -value
        last_segment = self._id.split("-")[-1]
        if last_segment.isdigit() and "-value" not in self._id:
            return f"#{self._id}-value"
        return f"#{self._id}"


class StreamFieldHelper:
    """
    Helper class for interacting with StreamField blocks in Wagtail admin.

    Provides a fluent API for navigating and manipulating StreamField blocks,
    including StructBlocks, ListBlocks, and deeply nested structures.

    Example:
        page_admin = PageAdminPage(page, base_url)
        page_admin.edit_page(page_id)

        sf = StreamFieldHelper(page, "body")

        # Add and fill a simple block
        index = sf.add_block("Heading")
        sf.block(index).fill("My Heading")

        # Work with StructBlock
        index = sf.add_block("Hero Section")
        sf.block(index).struct("title").fill("Welcome")
        sf.block(index).struct("subtitle").fill("To our site")

        # Work with ListBlock containing StructBlocks
        index = sf.add_block("Links")
        sf.block(index).item(0).struct("title").fill("Google")
        sf.block(index).item(0).struct("url").fill("https://google.com")

        # Deep nesting
        sf.block(0).item(0).struct("cards").item(0).struct("name").fill("Card")

    Attributes:
        page: The Playwright Page instance
        field_name: The name of the StreamField (e.g., "body")
    """

    def __init__(self, page: Page, field_name: str = "body") -> None:
        """
        Initialize the StreamFieldHelper.

        Args:
            page: Playwright Page instance (browser page)
            field_name: The name of the StreamField in the model (default: "body")
        """
        self.page = page
        self.field_name = field_name

    def block(self, index: int) -> BlockPath:
        """
        Get a BlockPath for a block at the specified index.

        This is the entry point for the fluent API. Chain methods like
        struct(), item(), fill(), and value() to navigate and interact
        with nested block structures.

        Args:
            index: The block index (0-based)

        Returns:
            BlockPath: A fluent builder for navigating the block structure

        Example:
            sf.block(0).fill("Simple value")
            sf.block(0).struct("title").fill("Struct field")
            sf.block(0).item(0).struct("name").fill("List item field")
        """
        return BlockPath(self, f"{self.field_name}-{index}")

    def _get_add_button(self):
        """Get the add block button for this StreamField (last one to append)."""
        panel_selector = f"#panel-child-content-{self.field_name}-section"
        panel = self.page.locator(panel_selector)
        return panel.locator(".c-sf-add-button").last

    def _get_block_count(self) -> int:
        """Get the current number of blocks in the StreamField."""
        count_input = self.page.locator(f"input[name='{self.field_name}-count']")
        if count_input.count() == 0:
            return 0
        value = count_input.input_value()
        return int(value) if value else 0

    def add_block(self, block_type: str) -> int:
        """
        Add a new block to the StreamField.

        Opens the block chooser menu, selects the specified block type,
        and returns the index of the newly added block.

        Args:
            block_type: The display name of the block type (e.g., "Heading",
                "Paragraph", "Quote"). This should match the label shown in
                the block chooser menu.

        Returns:
            int: The index of the newly added block (0-based).

        Example:
            sf = StreamFieldHelper(page, "body")
            index = sf.add_block("Heading")
            sf.block(index).fill("My Heading")
        """
        current_count = self._get_block_count()

        add_button = self._get_add_button()
        add_button.click()

        self.page.locator(".w-combobox__menu").wait_for(state="visible")

        # Use exact matching to avoid partial matches (e.g., "Section" vs "Hero")
        option = self.page.get_by_role("option", name=block_type, exact=True)
        option.click()

        self.page.wait_for_timeout(300)

        return current_count

    def get_block_count(self) -> int:
        """
        Get the number of blocks in the StreamField.

        Returns:
            int: The number of blocks currently in the StreamField.
        """
        return self._get_block_count()

    def get_block_type(self, index: int) -> str:
        """
        Get the type of a block at the specified index.

        Args:
            index: The block index (0-based)

        Returns:
            str: The block type identifier (e.g., "heading", "paragraph")
        """
        type_input = self.page.locator(f"input[name='{self.field_name}-{index}-type']")
        return type_input.input_value()

    def select_from_chooser(self, title: str) -> None:
        """
        Select an item from an open chooser modal by title.

        Call this after BlockPath.click_chooser() to select a specific item.

        Args:
            title: The title of the item to select

        Example:
            sf.block(0).struct("image").click_chooser()
            sf.select_from_chooser("My Image")
        """
        modal = self.page.locator("[data-chooser-modal]")
        modal.wait_for(state="visible")

        item = modal.locator(f"[data-title='{title}']").first
        if item.count() > 0:
            item.click()
        else:
            link = modal.get_by_role("link", name=title).first
            if link.count() > 0:
                link.click()

        self.page.wait_for_timeout(300)

    # Legacy methods for backward compatibility

    def fill_block(self, index: int, value: str) -> None:
        """
        Fill a simple block with a value.

        Deprecated: Use sf.block(index).fill(value) instead.
        """
        self.block(index).fill(value)

    def fill_struct_field(self, block_index: int, field_name: str, value: str) -> None:
        """
        Fill a field within a StructBlock.

        Deprecated: Use sf.block(index).struct(field_name).fill(value) instead.
        """
        self.block(block_index).struct(field_name).fill(value)

    def get_struct_field_value(self, block_index: int, field_name: str) -> str:
        """
        Get the value of a field within a StructBlock.

        Deprecated: Use sf.block(index).struct(field_name).value() instead.
        """
        return self.block(block_index).struct(field_name).value()

    def get_list_item_count(self, block_index: int) -> int:
        """
        Get the number of items in a ListBlock.

        Deprecated: Use sf.block(index).item_count() instead.
        """
        return self.block(block_index).item_count()

    def fill_list_item(self, block_index: int, item_index: int, value: str) -> None:
        """
        Fill a simple ListBlock item.

        Deprecated: Use sf.block(index).item(item_index).fill(value) instead.
        """
        self.block(block_index).item(item_index).fill(value)

    def fill_list_item_field(
        self, block_index: int, item_index: int, field_name: str, value: str
    ) -> None:
        """
        Fill a field within a StructBlock inside a ListBlock.

        Deprecated: Use sf.block(index).item(i).struct(field).fill(value) instead.
        """
        self.block(block_index).item(item_index).struct(field_name).fill(value)

    def get_list_item_field_value(
        self, block_index: int, item_index: int, field_name: str
    ) -> str:
        """
        Get the value of a field within a StructBlock inside a ListBlock.

        Deprecated: Use sf.block(index).item(i).struct(field).value() instead.
        """
        return self.block(block_index).item(item_index).struct(field_name).value()

    def click_image_chooser(
        self, block_index: int, field_name: str | None = None
    ) -> None:
        """
        Click the image chooser button.

        Deprecated: Use sf.block(index).click_chooser() or
        sf.block(index).struct(field).click_chooser() instead.
        """
        if field_name:
            self.block(block_index).struct(field_name).click_chooser()
        else:
            self.block(block_index).click_chooser()

    def select_image_from_chooser(self, image_title: str) -> None:
        """
        Select an image from the chooser modal.

        Deprecated: Use sf.select_from_chooser(title) instead.
        """
        self.select_from_chooser(image_title)

    def add_list_item(self, block_index: int) -> int:
        """
        Add a new item to a ListBlock.

        Deprecated: Use sf.block(index).add_item() instead.
        """
        return self.block(block_index).add_item()
