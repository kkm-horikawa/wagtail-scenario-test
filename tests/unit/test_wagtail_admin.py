"""Unit tests for WagtailAdminPage."""

from wagtail_scenario_test.page_objects.wagtail_admin import WagtailAdminPage


class TestWagtailAdminPageUrls:
    """Tests for WagtailAdminPage URL constants."""

    def test_admin_root_url(self):
        """ADMIN_ROOT should be /admin/."""
        assert WagtailAdminPage.ADMIN_ROOT == "/admin/"

    def test_login_url(self):
        """LOGIN_URL should be /admin/login/."""
        assert WagtailAdminPage.LOGIN_URL == "/admin/login/"

    def test_logout_url(self):
        """LOGOUT_URL should be /admin/logout/."""
        assert WagtailAdminPage.LOGOUT_URL == "/admin/logout/"


class TestWagtailAdminPageAuth:
    """Tests for WagtailAdminPage authentication methods."""

    def test_login(self, mock_page, test_url):
        """login should fill credentials and submit."""
        admin = WagtailAdminPage(mock_page, test_url)

        admin.login("admin", "password123")

        # Check navigation to login page
        mock_page.goto.assert_called_once_with(f"{test_url}/admin/login/")

        # Check form filling
        assert mock_page.get_by_label.call_count == 2
        mock_page.get_by_label.assert_any_call("Username")
        mock_page.get_by_label.assert_any_call("Password")

        # Check button click
        mock_page.get_by_role.assert_called_once_with("button", name="Sign in")

        # Check wait for redirect
        mock_page.wait_for_url.assert_called_once_with("**/admin/**")

    def test_logout(self, mock_page, test_url):
        """logout should navigate to logout URL."""
        admin = WagtailAdminPage(mock_page, test_url)

        admin.logout()

        # Should navigate to logout URL
        mock_page.goto.assert_called_with(f"{test_url}/admin/logout/")
        # Should wait for navigation
        mock_page.wait_for_load_state.assert_called()

    def test_is_logged_in_returns_true(self, mock_page, test_url):
        """is_logged_in should return True when on admin page."""
        mock_page.url = f"{test_url}/admin/"
        admin = WagtailAdminPage(mock_page, test_url)

        result = admin.is_logged_in()

        assert result is True

    def test_is_logged_in_returns_false(self, mock_page, test_url):
        """is_logged_in should return False when on login page."""
        mock_page.url = f"{test_url}/admin/login/"
        admin = WagtailAdminPage(mock_page, test_url)

        result = admin.is_logged_in()

        assert result is False


class TestWagtailAdminPageNavigation:
    """Tests for WagtailAdminPage navigation methods."""

    def test_go_to_dashboard(self, mock_page, test_url):
        """go_to_dashboard should navigate to admin root."""
        admin = WagtailAdminPage(mock_page, test_url)

        admin.go_to_dashboard()

        mock_page.goto.assert_called_once_with(f"{test_url}/admin/")

    def test_open_sidebar_menu(self, mock_page, test_url):
        """open_sidebar_menu should click menu button."""
        admin = WagtailAdminPage(mock_page, test_url)

        admin.open_sidebar_menu("Snippets")

        mock_page.get_by_role.assert_called_once_with("button", name="Snippets")
        mock_page.get_by_role.return_value.click.assert_called_once()

    def test_click_sidebar_link(self, mock_page, test_url):
        """click_sidebar_link should click link."""
        admin = WagtailAdminPage(mock_page, test_url)

        admin.click_sidebar_link("Pages")

        mock_page.get_by_role.assert_called_once_with("link", name="Pages")
        mock_page.get_by_role.return_value.click.assert_called_once()


class TestWagtailAdminPageSearch:
    """Tests for WagtailAdminPage search methods."""

    def test_search(self, mock_page, test_url):
        """search should fill search input and press Enter."""
        admin = WagtailAdminPage(mock_page, test_url)
        search_input = mock_page.locator.return_value

        admin.search("test query")

        mock_page.locator.assert_called_with("#id_q")
        search_input.fill.assert_called_once_with("test query")
        search_input.press.assert_called_once_with("Enter")

    def test_global_search(self, mock_page, test_url):
        """global_search should use sidebar search."""
        admin = WagtailAdminPage(mock_page, test_url)

        admin.global_search("my search")

        mock_page.get_by_placeholder.assert_called_with("Search")


class TestWagtailAdminPageNotifications:
    """Tests for WagtailAdminPage notification methods."""

    def test_get_success_message_returns_text(self, mock_page, test_url):
        """get_success_message should return message text."""
        admin = WagtailAdminPage(mock_page, test_url)
        locator = mock_page.locator.return_value
        locator.count.return_value = 1
        locator.first.text_content.return_value = "Saved successfully"

        result = admin.get_success_message()

        mock_page.locator.assert_called_with(".w-message--success")
        assert result == "Saved successfully"

    def test_get_success_message_returns_none(self, mock_page, test_url):
        """get_success_message should return None if no message."""
        admin = WagtailAdminPage(mock_page, test_url)
        mock_page.locator.return_value.count.return_value = 0

        result = admin.get_success_message()

        assert result is None

    def test_get_error_message_returns_text(self, mock_page, test_url):
        """get_error_message should return message text."""
        admin = WagtailAdminPage(mock_page, test_url)
        locator = mock_page.locator.return_value
        locator.count.return_value = 1
        locator.first.text_content.return_value = "Error occurred"

        result = admin.get_error_message()

        mock_page.locator.assert_called_with(".w-message--error")
        assert result == "Error occurred"

    def test_get_error_message_returns_none(self, mock_page, test_url):
        """get_error_message should return None if no message."""
        admin = WagtailAdminPage(mock_page, test_url)
        mock_page.locator.return_value.count.return_value = 0

        result = admin.get_error_message()

        assert result is None

    def test_assert_success_message(self, mock_page, test_url, mock_playwright_expect):
        """assert_success_message should check for success message."""
        admin = WagtailAdminPage(mock_page, test_url)

        admin.assert_success_message()

        mock_page.locator.assert_called()
        mock_playwright_expect.assert_called()

    def test_assert_success_message_with_contains(
        self, mock_page, test_url, mock_playwright_expect
    ):
        """assert_success_message should check message content."""
        admin = WagtailAdminPage(mock_page, test_url)

        admin.assert_success_message(contains="Created")

        mock_page.locator.assert_called()

    def test_assert_error_message(self, mock_page, test_url, mock_playwright_expect):
        """assert_error_message should check for error message."""
        admin = WagtailAdminPage(mock_page, test_url)

        admin.assert_error_message()

        mock_page.locator.assert_called_with(".w-message--error")

    def test_assert_error_message_with_contains(
        self, mock_page, test_url, mock_playwright_expect
    ):
        """assert_error_message should check message content."""
        admin = WagtailAdminPage(mock_page, test_url)

        admin.assert_error_message(contains="failed")

        mock_page.locator.assert_called()
