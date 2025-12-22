"""Unit tests for BasePage."""

from wagtail_scenario_test.page_objects.base import BasePage


class TestBasePageInit:
    """Tests for BasePage initialization."""

    def test_init_stores_page_and_base_url(self, mock_page):
        """BasePage should store page and base_url."""
        base = BasePage(mock_page, "http://localhost:8000")

        assert base.page is mock_page
        assert base.base_url == "http://localhost:8000"

    def test_init_strips_trailing_slash(self, mock_page):
        """BasePage should strip trailing slash from base_url."""
        base = BasePage(mock_page, "http://localhost:8000/")

        assert base.base_url == "http://localhost:8000"


class TestBasePageNavigation:
    """Tests for BasePage navigation methods."""

    def test_goto_navigates_to_path(self, mock_page, test_url):
        """goto should navigate to base_url + path."""
        base = BasePage(mock_page, test_url)

        base.goto("/admin/")

        mock_page.goto.assert_called_once_with("http://localhost:8000/admin/")

    def test_current_path_returns_path_without_base(self, mock_page, test_url):
        """current_path should return URL path without base_url."""
        mock_page.url = "http://localhost:8000/admin/snippets/"
        base = BasePage(mock_page, test_url)

        result = base.current_path()

        assert result == "/admin/snippets/"

    def test_reload_reloads_page(self, mock_page, test_url):
        """reload should reload the page."""
        base = BasePage(mock_page, test_url)

        base.reload()

        mock_page.reload.assert_called_once()


class TestBasePageWaiting:
    """Tests for BasePage waiting utilities."""

    def test_wait_for_navigation(self, mock_page, test_url):
        """wait_for_navigation should wait for networkidle."""
        base = BasePage(mock_page, test_url)

        base.wait_for_navigation()

        mock_page.wait_for_load_state.assert_called_once_with(
            "networkidle", timeout=30000
        )

    def test_wait_for_navigation_with_custom_timeout(self, mock_page, test_url):
        """wait_for_navigation should accept custom timeout."""
        base = BasePage(mock_page, test_url)

        base.wait_for_navigation(timeout=5000)

        mock_page.wait_for_load_state.assert_called_once_with(
            "networkidle", timeout=5000
        )

    def test_wait_for_element(self, mock_page, test_url):
        """wait_for_element should wait for element visibility."""
        base = BasePage(mock_page, test_url)
        locator = mock_page.locator.return_value

        result = base.wait_for_element("#my-element")

        mock_page.locator.assert_called_once_with("#my-element")
        locator.wait_for.assert_called_once_with(state="visible", timeout=30000)
        assert result is locator

    def test_wait_for_element_with_custom_timeout(self, mock_page, test_url):
        """wait_for_element should accept custom timeout."""
        base = BasePage(mock_page, test_url)
        locator = mock_page.locator.return_value

        base.wait_for_element("#my-element", timeout=5000)

        locator.wait_for.assert_called_once_with(state="visible", timeout=5000)

    def test_wait_for_text(self, mock_page, test_url):
        """wait_for_text should wait for text visibility."""
        base = BasePage(mock_page, test_url)
        locator = mock_page.get_by_text.return_value

        base.wait_for_text("Hello World")

        mock_page.get_by_text.assert_called_once_with("Hello World")
        locator.wait_for.assert_called_once_with(state="visible", timeout=30000)

    def test_wait_for_text_with_custom_timeout(self, mock_page, test_url):
        """wait_for_text should accept custom timeout."""
        base = BasePage(mock_page, test_url)
        locator = mock_page.get_by_text.return_value

        base.wait_for_text("Hello", timeout=5000)

        locator.wait_for.assert_called_once_with(state="visible", timeout=5000)


class TestBasePageInteractions:
    """Tests for BasePage common interactions."""

    def test_click_button(self, mock_page, test_url):
        """click_button should click button by name."""
        base = BasePage(mock_page, test_url)

        base.click_button("Submit")

        mock_page.get_by_role.assert_called_once_with("button", name="Submit")
        mock_page.get_by_role.return_value.click.assert_called_once()

    def test_click_link(self, mock_page, test_url):
        """click_link should click link by name."""
        base = BasePage(mock_page, test_url)

        base.click_link("Home")

        mock_page.get_by_role.assert_called_once_with("link", name="Home")
        mock_page.get_by_role.return_value.click.assert_called_once()

    def test_fill_field(self, mock_page, test_url):
        """fill_field should fill textbox by label."""
        base = BasePage(mock_page, test_url)

        base.fill_field("Username", "admin")

        mock_page.get_by_role.assert_called_once_with("textbox", name="Username")
        mock_page.get_by_role.return_value.fill.assert_called_once_with("admin")

    def test_fill_field_by_id_with_hash(self, mock_page, test_url):
        """fill_field_by_id should work with # prefix."""
        base = BasePage(mock_page, test_url)

        base.fill_field_by_id("#id_name", "Test")

        mock_page.locator.assert_called_once_with("#id_name")
        mock_page.locator.return_value.fill.assert_called_once_with("Test")

    def test_fill_field_by_id_without_hash(self, mock_page, test_url):
        """fill_field_by_id should add # prefix if missing."""
        base = BasePage(mock_page, test_url)

        base.fill_field_by_id("id_name", "Test")

        mock_page.locator.assert_called_once_with("#id_name")
        mock_page.locator.return_value.fill.assert_called_once_with("Test")

    def test_clear_and_fill(self, mock_page, test_url):
        """clear_and_fill should triple-click then fill."""
        base = BasePage(mock_page, test_url)
        locator = mock_page.locator.return_value

        base.clear_and_fill("#field", "new value")

        mock_page.locator.assert_called_once_with("#field")
        locator.click.assert_called_once_with(click_count=3)
        locator.fill.assert_called_once_with("new value")

    def test_select_option(self, mock_page, test_url):
        """select_option should select dropdown option."""
        base = BasePage(mock_page, test_url)

        base.select_option("Country", "jp")

        mock_page.get_by_label.assert_called_once_with("Country")
        mock_page.get_by_label.return_value.select_option.assert_called_once_with("jp")

    def test_check_checkbox(self, mock_page, test_url):
        """check_checkbox should check checkbox by label."""
        base = BasePage(mock_page, test_url)

        base.check_checkbox("Agree to terms")

        mock_page.get_by_label.assert_called_once_with("Agree to terms")
        mock_page.get_by_label.return_value.check.assert_called_once()

    def test_uncheck_checkbox(self, mock_page, test_url):
        """uncheck_checkbox should uncheck checkbox by label."""
        base = BasePage(mock_page, test_url)

        base.uncheck_checkbox("Subscribe")

        mock_page.get_by_label.assert_called_once_with("Subscribe")
        mock_page.get_by_label.return_value.uncheck.assert_called_once()


class TestBasePageAssertions:
    """Tests for BasePage assertion methods."""

    def test_assert_visible(self, mock_page, test_url, mock_playwright_expect):
        """assert_visible should check text visibility."""
        base = BasePage(mock_page, test_url)

        base.assert_visible("Success!")

        mock_page.get_by_text.assert_called_once_with("Success!")
        mock_playwright_expect.assert_called()

    def test_assert_not_visible(self, mock_page, test_url, mock_playwright_expect):
        """assert_not_visible should check text is not visible."""
        base = BasePage(mock_page, test_url)

        base.assert_not_visible("Error")

        mock_page.get_by_text.assert_called_once_with("Error")

    def test_assert_url_contains(self, mock_page, test_url, mock_playwright_expect):
        """assert_url_contains should check URL pattern."""
        base = BasePage(mock_page, test_url)

        base.assert_url_contains("/admin/")

        mock_playwright_expect.assert_called()

    def test_assert_title(self, mock_page, test_url, mock_playwright_expect):
        """assert_title should check page title."""
        base = BasePage(mock_page, test_url)

        base.assert_title("Home - Wagtail")

        mock_playwright_expect.assert_called()

    def test_assert_element_visible(self, mock_page, test_url, mock_playwright_expect):
        """assert_element_visible should check element visibility."""
        base = BasePage(mock_page, test_url)

        base.assert_element_visible(".success-message")

        mock_page.locator.assert_called_once_with(".success-message")

    def test_assert_element_not_visible(
        self, mock_page, test_url, mock_playwright_expect
    ):
        """assert_element_not_visible should check element not visible."""
        base = BasePage(mock_page, test_url)

        base.assert_element_not_visible(".error-message")

        mock_page.locator.assert_called_once_with(".error-message")


class TestBasePageDebugging:
    """Tests for BasePage debugging methods."""

    def test_screenshot(self, mock_page, test_url):
        """screenshot should take and save screenshot."""
        base = BasePage(mock_page, test_url)

        result = base.screenshot("test-screenshot")

        mock_page.screenshot.assert_called_once_with(
            path="screenshots/test-screenshot.png"
        )
        assert result == b"fake-screenshot-data"

    def test_debug_pause(self, mock_page, test_url):
        """debug_pause should pause execution."""
        base = BasePage(mock_page, test_url)

        base.debug_pause()

        mock_page.pause.assert_called_once()

    def test_get_page_content(self, mock_page, test_url):
        """get_page_content should return HTML content."""
        base = BasePage(mock_page, test_url)

        result = base.get_page_content()

        mock_page.content.assert_called_once()
        assert result == "<html><body>Test</body></html>"

    def test_get_visible_text(self, mock_page, test_url):
        """get_visible_text should return body text."""
        base = BasePage(mock_page, test_url)

        result = base.get_visible_text()

        mock_page.locator.assert_called_once_with("body")
        assert result == "Page content"


class TestBasePageWaitForText:
    """Tests for wait_for_text method."""

    def test_wait_for_text(self, mock_page, test_url):
        """wait_for_text should wait for text visibility."""
        base = BasePage(mock_page, test_url)
        locator = mock_page.get_by_text.return_value

        base.wait_for_text("Hello World")

        mock_page.get_by_text.assert_called_once_with("Hello World")
        locator.wait_for.assert_called_once_with(state="visible", timeout=30000)

    def test_wait_for_text_with_custom_timeout(self, mock_page, test_url):
        """wait_for_text should accept custom timeout."""
        base = BasePage(mock_page, test_url)
        locator = mock_page.get_by_text.return_value

        base.wait_for_text("Hello", timeout=5000)

        locator.wait_for.assert_called_once_with(state="visible", timeout=5000)


class TestBasePageAssertTitle:
    """Tests for assert_title method."""

    def test_assert_title(self, mock_page, test_url, mock_playwright_expect):
        """assert_title should check page title."""
        base = BasePage(mock_page, test_url)

        base.assert_title("Home - Wagtail")

        mock_playwright_expect.assert_called_with(mock_page)


class TestBasePageAssertElementVisibility:
    """Tests for element visibility assertions."""

    def test_assert_element_visible(self, mock_page, test_url, mock_playwright_expect):
        """assert_element_visible should check element visibility."""
        base = BasePage(mock_page, test_url)

        base.assert_element_visible(".success-message")

        mock_page.locator.assert_called_once_with(".success-message")
        mock_playwright_expect.assert_called()

    def test_assert_element_not_visible(
        self, mock_page, test_url, mock_playwright_expect
    ):
        """assert_element_not_visible should check element not visible."""
        base = BasePage(mock_page, test_url)

        base.assert_element_not_visible(".error-message")

        mock_page.locator.assert_called_once_with(".error-message")
