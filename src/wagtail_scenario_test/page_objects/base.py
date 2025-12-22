"""
Base Page Object class for E2E testing.

Page Objects encapsulate UI interactions and provide a clean API
for tests. When UI changes, only the Page Object needs to be updated.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from playwright.sync_api import Locator, expect

if TYPE_CHECKING:
    from playwright.sync_api import Page


class BasePage:
    """
    Base class for all Page Objects.

    Provides common utilities and patterns for interacting with pages.

    Attributes:
        page: The Playwright Page instance
        base_url: The base URL for the application

    Example:
        class MyPage(BasePage):
            def do_something(self):
                self.goto("/my-path/")
                self.click_button("Submit")
    """

    def __init__(self, page: Page, base_url: str) -> None:
        """
        Initialize the Page Object.

        Args:
            page: Playwright Page instance (usually from authenticated_page fixture)
            base_url: Base URL of the test server (usually from live_server.url)
        """
        self.page = page
        self.base_url = base_url.rstrip("/")

    # =========================================================================
    # Navigation
    # =========================================================================

    def goto(self, path: str) -> None:
        """
        Navigate to a path relative to base_url.

        Args:
            path: URL path starting with /
        """
        url = f"{self.base_url}{path}"
        self.page.goto(url)

    def current_path(self) -> str:
        """Return the current URL path (without base_url)."""
        return self.page.url.replace(self.base_url, "")

    def reload(self) -> None:
        """Reload the current page."""
        self.page.reload()

    # =========================================================================
    # Waiting utilities
    # =========================================================================

    def wait_for_navigation(self, timeout: int = 30000) -> None:
        """
        Wait for navigation to complete.

        Args:
            timeout: Maximum wait time in milliseconds
        """
        self.page.wait_for_load_state("networkidle", timeout=timeout)

    def wait_for_element(self, selector: str, timeout: int = 30000) -> Locator:
        """
        Wait for an element to be visible.

        Args:
            selector: CSS selector
            timeout: Maximum wait time in milliseconds

        Returns:
            The Locator for the element
        """
        locator = self.page.locator(selector)
        locator.wait_for(state="visible", timeout=timeout)
        return locator

    def wait_for_text(self, text: str, timeout: int = 30000) -> None:
        """
        Wait for text to appear on the page.

        Args:
            text: Text to wait for
            timeout: Maximum wait time in milliseconds
        """
        self.page.get_by_text(text).wait_for(state="visible", timeout=timeout)

    # =========================================================================
    # Common interactions
    # =========================================================================

    def click_button(self, name: str) -> None:
        """
        Click a button by its accessible name.

        Args:
            name: Button text or aria-label
        """
        self.page.get_by_role("button", name=name).click()

    def click_link(self, name: str) -> None:
        """
        Click a link by its accessible name.

        Args:
            name: Link text or aria-label
        """
        self.page.get_by_role("link", name=name).click()

    def fill_field(self, label: str, value: str) -> None:
        """
        Fill a form field by its label.

        Args:
            label: Field label text
            value: Value to fill
        """
        field = self.page.get_by_role("textbox", name=label)
        field.fill(value)

    def fill_field_by_id(self, field_id: str, value: str) -> None:
        """
        Fill a form field by its ID.

        Args:
            field_id: The id attribute of the field (with or without #)
            value: Value to fill
        """
        selector = field_id if field_id.startswith("#") else f"#{field_id}"
        field = self.page.locator(selector)
        field.fill(value)

    def clear_and_fill(self, selector: str, value: str) -> None:
        """
        Clear a field and fill it with a new value.

        Uses triple-click to select all text before filling.

        Args:
            selector: CSS selector for the field
            value: Value to fill
        """
        field = self.page.locator(selector)
        field.click(click_count=3)  # Triple-click to select all
        field.fill(value)

    def select_option(self, label: str, value: str) -> None:
        """
        Select an option from a dropdown by label.

        Args:
            label: Dropdown label text
            value: Option value to select
        """
        self.page.get_by_label(label).select_option(value)

    def check_checkbox(self, label: str) -> None:
        """
        Check a checkbox by its label.

        Args:
            label: Checkbox label text
        """
        self.page.get_by_label(label).check()

    def uncheck_checkbox(self, label: str) -> None:
        """
        Uncheck a checkbox by its label.

        Args:
            label: Checkbox label text
        """
        self.page.get_by_label(label).uncheck()

    # =========================================================================
    # Assertions
    # =========================================================================

    def assert_visible(self, text: str) -> None:
        """
        Assert that text is visible on the page.

        Args:
            text: Text to check for
        """
        expect(self.page.get_by_text(text)).to_be_visible()

    def assert_not_visible(self, text: str) -> None:
        """
        Assert that text is not visible on the page.

        Args:
            text: Text to check is not present
        """
        expect(self.page.get_by_text(text)).not_to_be_visible()

    def assert_url_contains(self, path: str) -> None:
        """
        Assert that the current URL contains the given path.

        Args:
            path: Path fragment to check for
        """
        expect(self.page).to_have_url(f"**{path}**")

    def assert_title(self, title: str) -> None:
        """
        Assert the page title.

        Args:
            title: Expected page title
        """
        expect(self.page).to_have_title(title)

    def assert_element_visible(self, selector: str) -> None:
        """
        Assert that an element is visible.

        Args:
            selector: CSS selector
        """
        expect(self.page.locator(selector)).to_be_visible()

    def assert_element_not_visible(self, selector: str) -> None:
        """
        Assert that an element is not visible.

        Args:
            selector: CSS selector
        """
        expect(self.page.locator(selector)).not_to_be_visible()

    # =========================================================================
    # Screenshots and debugging
    # =========================================================================

    def screenshot(self, name: str) -> bytes:
        """
        Take a screenshot for debugging.

        Args:
            name: Screenshot filename (without extension)

        Returns:
            Screenshot bytes
        """
        return self.page.screenshot(path=f"screenshots/{name}.png")

    def debug_pause(self) -> None:
        """Pause execution for debugging (use with headed mode)."""
        self.page.pause()

    def get_page_content(self) -> str:
        """
        Get the full page HTML content.

        Returns:
            Page HTML as string
        """
        return self.page.content()

    def get_visible_text(self) -> str:
        """
        Get all visible text on the page.

        Returns:
            Visible text content
        """
        return self.page.locator("body").inner_text()

    # =========================================================================
    # Storage state (authentication persistence)
    # =========================================================================

    def save_storage_state(self, path: str | Path) -> Path:
        """
        Save browser storage state (cookies, localStorage) to a file.

        This allows reusing authentication state across tests,
        significantly speeding up test execution.

        Args:
            path: File path to save state to (JSON format)

        Returns:
            Path to the saved state file

        Example:
            >>> page.save_storage_state("auth_state.json")
            >>> # Later, use this state with browser.new_context(storage_state=...)
        """
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        self.page.context.storage_state(path=str(path))
        return path
