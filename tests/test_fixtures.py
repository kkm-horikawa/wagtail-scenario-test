"""Tests for pytest fixtures."""

from unittest.mock import MagicMock

import pytest


@pytest.mark.django_db
class TestServerUrlFixture:
    """Tests for server_url fixture."""

    def test_returns_live_server_url(self, server_url, live_server):
        """server_url should return live_server.url as string."""
        assert server_url == str(live_server.url)
        assert isinstance(server_url, str)

    def test_returns_string_type(self, server_url):
        """server_url should return a string."""
        assert isinstance(server_url, str)
        assert server_url.startswith("http")


class TestAdminCredentialsFixture:
    """Tests for admin_credentials fixture."""

    def test_returns_default_credentials(self, admin_credentials):
        """admin_credentials should return default credentials."""
        assert admin_credentials == {
            "username": "e2e_admin",
            "password": "e2e_password_123",
        }

    def test_returns_dict_with_username_and_password(self, admin_credentials):
        """admin_credentials should return dict with required keys."""
        assert "username" in admin_credentials
        assert "password" in admin_credentials


@pytest.mark.django_db
class TestWagtailSiteFixture:
    """Tests for wagtail_site fixture."""

    def test_creates_locale(self, wagtail_site):
        """wagtail_site should create default locale."""
        from wagtail.models import Locale

        assert Locale.objects.exists()

    def test_creates_root_page(self, wagtail_site):
        """wagtail_site should ensure root page exists."""
        from wagtail.models import Page

        assert Page.objects.filter(depth=1).exists()

    def test_creates_site(self, wagtail_site):
        """wagtail_site should create site."""
        assert wagtail_site is not None
        assert wagtail_site.hostname == "localhost"

    def test_site_is_default(self, wagtail_site):
        """wagtail_site should create default site."""
        assert wagtail_site.is_default_site is True


@pytest.mark.django_db
class TestAdminUserE2EFixture:
    """Tests for admin_user_e2e fixture."""

    def test_creates_admin_user(self, admin_user_e2e):
        """admin_user_e2e should create admin user."""
        assert admin_user_e2e is not None
        assert admin_user_e2e.username == "e2e_admin"

    def test_user_is_staff(self, admin_user_e2e):
        """admin_user_e2e should create staff user."""
        assert admin_user_e2e.is_staff is True

    def test_user_is_superuser(self, admin_user_e2e):
        """admin_user_e2e should create superuser."""
        assert admin_user_e2e.is_superuser is True

    def test_sets_password(self, admin_user_e2e):
        """admin_user_e2e should set password."""
        assert admin_user_e2e.check_password("e2e_password_123")


class TestAuthenticatedPageFunction:
    """Tests for authenticated_page fixture function logic."""

    def test_navigates_to_login(self):
        """authenticated_page should navigate to login page."""
        from wagtail_scenario_test.fixtures import authenticated_page

        mock_page = MagicMock()
        server_url = "http://localhost:8000"
        credentials = {"username": "admin", "password": "pass"}

        # Get the internal function (unwrap the fixture)
        authenticated_page.__wrapped__(mock_page, server_url, None, credentials)

        mock_page.goto.assert_called_once_with(f"{server_url}/admin/login/")

    def test_fills_username(self):
        """authenticated_page should fill username."""
        from wagtail_scenario_test.fixtures import authenticated_page

        mock_page = MagicMock()
        server_url = "http://localhost:8000"
        credentials = {"username": "admin", "password": "pass"}

        authenticated_page.__wrapped__(mock_page, server_url, None, credentials)

        mock_page.get_by_label.assert_any_call("Username")

    def test_fills_password(self):
        """authenticated_page should fill password."""
        from wagtail_scenario_test.fixtures import authenticated_page

        mock_page = MagicMock()
        server_url = "http://localhost:8000"
        credentials = {"username": "admin", "password": "pass"}

        authenticated_page.__wrapped__(mock_page, server_url, None, credentials)

        mock_page.get_by_label.assert_any_call("Password")

    def test_clicks_sign_in(self):
        """authenticated_page should click Sign in button."""
        from wagtail_scenario_test.fixtures import authenticated_page

        mock_page = MagicMock()
        server_url = "http://localhost:8000"
        credentials = {"username": "admin", "password": "pass"}

        authenticated_page.__wrapped__(mock_page, server_url, None, credentials)

        mock_page.get_by_role.assert_called_once_with("button", name="Sign in")

    def test_waits_for_redirect(self):
        """authenticated_page should wait for admin redirect."""
        from wagtail_scenario_test.fixtures import authenticated_page

        mock_page = MagicMock()
        server_url = "http://localhost:8000"
        credentials = {"username": "admin", "password": "pass"}

        authenticated_page.__wrapped__(mock_page, server_url, None, credentials)

        mock_page.wait_for_url.assert_called_once_with(f"{server_url}/admin/**")

    def test_returns_page(self):
        """authenticated_page should return the page."""
        from wagtail_scenario_test.fixtures import authenticated_page

        mock_page = MagicMock()
        server_url = "http://localhost:8000"
        credentials = {"username": "admin", "password": "pass"}

        result = authenticated_page.__wrapped__(
            mock_page, server_url, None, credentials
        )

        assert result is mock_page


class TestPytestConfigure:
    """Tests for pytest_configure hook."""

    def test_registers_e2e_marker(self):
        """pytest_configure should register e2e marker."""
        from wagtail_scenario_test.fixtures import pytest_configure

        mock_config = MagicMock()

        pytest_configure(mock_config)

        # Check that addinivalue_line was called for e2e marker
        calls = [str(c) for c in mock_config.addinivalue_line.call_args_list]
        assert any("e2e" in str(c) for c in calls)

    def test_registers_slow_marker(self):
        """pytest_configure should register slow marker."""
        from wagtail_scenario_test.fixtures import pytest_configure

        mock_config = MagicMock()

        pytest_configure(mock_config)

        # Check that addinivalue_line was called for slow marker
        calls = [str(c) for c in mock_config.addinivalue_line.call_args_list]
        assert any("slow" in str(c) for c in calls)
