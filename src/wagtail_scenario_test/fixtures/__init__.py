"""
Pytest fixtures for Wagtail E2E testing.

This module is registered as a pytest plugin via the pytest11 entry point.
When wagtail-scenario-test is installed, these fixtures are automatically
available in tests.

Available fixtures:
    - server_url: Base URL of the live test server
    - wagtail_site: Creates a Wagtail site with root page
    - admin_credentials: Returns default admin credentials
    - admin_user_e2e: Creates an admin user for E2E testing
    - authenticated_page: Playwright page logged into Wagtail admin

Usage:
    # In your conftest.py, the fixtures are automatically available
    def test_something(authenticated_page, server_url):
        authenticated_page.goto(f"{server_url}/admin/")
"""

import os

import pytest
from playwright.sync_api import Page

# Allow Django ORM in async context (required for Playwright + Django integration)
os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "1")


@pytest.fixture
def server_url(live_server) -> str:
    """
    Return the base URL of the live test server.

    This fixture depends on pytest-django's live_server fixture.

    Returns:
        str: The server URL (e.g., "http://localhost:8000")
    """
    return live_server.url


@pytest.fixture
def admin_credentials() -> dict[str, str]:
    """
    Return admin user credentials for E2E testing.

    Override this fixture to customize credentials.

    Returns:
        dict: Contains 'username' and 'password' keys
    """
    return {"username": "e2e_admin", "password": "e2e_password_123"}


@pytest.fixture
def wagtail_site(db):
    """
    Create a Wagtail site with root page for E2E testing.

    This fixture:
    1. Creates the default locale (required for Wagtail i18n)
    2. Gets or creates a root page
    3. Gets or creates a site

    Returns:
        Site: The Wagtail Site instance
    """
    from django.conf import settings

    from wagtail.models import Locale, Page, Site

    # Get the language code that Wagtail will use for the default locale
    language_code = settings.LANGUAGE_CODE

    # Try to get the content language variant Wagtail uses internally
    try:
        from wagtail.coreutils import get_supported_content_language_variant

        language_code = get_supported_content_language_variant(language_code)
    except (ImportError, LookupError):
        pass

    Locale.objects.get_or_create(language_code=language_code)

    # Get or create root page
    try:
        root = Page.objects.get(depth=1)
    except Page.DoesNotExist:
        root = Page.add_root(title="Root", slug="root")

    # Get or create site
    site, _ = Site.objects.get_or_create(
        hostname="localhost",
        defaults={
            "root_page": root,
            "is_default_site": True,
            "site_name": "Test Site",
        },
    )
    return site


@pytest.fixture
def admin_user_e2e(db, wagtail_site, admin_credentials):
    """
    Create an admin user for E2E testing.

    Uses get_or_create to avoid duplicate user errors when
    running multiple tests with transaction isolation.

    Args:
        db: pytest-django db fixture
        wagtail_site: Ensures site exists before creating user
        admin_credentials: Login credentials

    Returns:
        User: The admin user instance
    """
    from django.contrib.auth import get_user_model

    User = get_user_model()

    user, created = User.objects.get_or_create(
        username=admin_credentials["username"],
        defaults={
            "email": "e2e_admin@example.com",
            "is_staff": True,
            "is_superuser": True,
        },
    )
    if created:
        user.set_password(admin_credentials["password"])
        user.save()
    return user


@pytest.fixture
def authenticated_page(
    page: Page,
    server_url: str,
    admin_user_e2e,
    admin_credentials: dict[str, str],
) -> Page:
    """
    Return a Playwright page that is logged into Wagtail admin.

    This is the main fixture for E2E tests. It provides a browser
    page that is already authenticated as an admin user.

    Args:
        page: Playwright's page fixture
        server_url: The test server URL
        admin_user_e2e: Ensures admin user exists
        admin_credentials: Login credentials

    Returns:
        Page: Playwright page logged into admin

    Usage:
        def test_something(authenticated_page, server_url):
            authenticated_page.goto(f"{server_url}/admin/snippets/")
            # Already logged in
    """
    # Navigate to login page
    page.goto(f"{server_url}/admin/login/")

    # Fill login form
    page.get_by_label("Username").fill(admin_credentials["username"])
    page.get_by_label("Password").fill(admin_credentials["password"])
    page.get_by_role("button", name="Sign in").click()

    # Wait for redirect to admin dashboard
    page.wait_for_url(f"{server_url}/admin/**")

    return page


def pytest_configure(config):
    """Register custom markers for E2E tests."""
    config.addinivalue_line(
        "markers",
        "e2e: mark test as end-to-end test (requires browser)",
    )
    config.addinivalue_line(
        "markers",
        "slow: mark test as slow-running",
    )
