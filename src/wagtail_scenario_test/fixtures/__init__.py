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
    - storage_state_path: Path for storing authentication state
    - authenticated_browser_context: Session-scoped authenticated context

Usage:
    # In your conftest.py, the fixtures are automatically available
    def test_something(authenticated_page, server_url):
        authenticated_page.goto(f"{server_url}/admin/")
"""

import os
from collections.abc import Generator
from pathlib import Path

import pytest
from playwright.sync_api import BrowserContext, Page

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
    return str(live_server.url)


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


@pytest.fixture(scope="session")
def storage_state_path(tmp_path_factory) -> Path:
    """
    Return path for storing authentication state.

    Override this fixture to use a custom path.

    Returns:
        Path: Path to the storage state JSON file
    """
    base_path: Path = tmp_path_factory.mktemp("playwright")
    return base_path / "storage_state.json"


@pytest.fixture(scope="session")
def _authenticated_storage_state(
    browser,
    live_server,
    django_db_setup,
    django_db_blocker,
    storage_state_path: Path,
) -> Path:
    """
    Create and save authenticated storage state (session-scoped).

    This fixture logs in once per session and saves the browser state,
    allowing subsequent tests to skip the login process.

    Returns:
        Path: Path to the saved storage state file
    """
    from django.contrib.auth import get_user_model

    # Create admin user in database
    with django_db_blocker.unblock():
        User = get_user_model()
        user, created = User.objects.get_or_create(
            username="e2e_admin",
            defaults={
                "email": "e2e_admin@example.com",
                "is_staff": True,
                "is_superuser": True,
            },
        )
        if created:
            user.set_password("e2e_password_123")
            user.save()

    # Create context and login
    context = browser.new_context()
    page = context.new_page()

    server_url = str(live_server.url)
    page.goto(f"{server_url}/admin/login/")
    page.get_by_label("Username").fill("e2e_admin")
    page.get_by_label("Password").fill("e2e_password_123")
    page.get_by_role("button", name="Sign in").click()
    page.wait_for_url(f"{server_url}/admin/**")

    # Save storage state
    storage_state_path.parent.mkdir(parents=True, exist_ok=True)
    context.storage_state(path=str(storage_state_path))

    context.close()
    return storage_state_path


@pytest.fixture
def authenticated_browser_context(
    browser,
    _authenticated_storage_state: Path,
) -> Generator[BrowserContext, None, None]:
    """
    Return a browser context with pre-authenticated state.

    This fixture uses saved storage state to skip login,
    making tests faster when you need multiple pages or contexts.

    Usage:
        def test_multi_page(authenticated_browser_context, server_url):
            page1 = authenticated_browser_context.new_page()
            page2 = authenticated_browser_context.new_page()
            # Both pages are already logged in
    """
    context = browser.new_context(storage_state=str(_authenticated_storage_state))
    yield context
    context.close()


@pytest.fixture
def authenticated_page_fast(
    authenticated_browser_context: BrowserContext,
) -> Generator[Page, None, None]:
    """
    Return a Playwright page with pre-authenticated state (faster).

    This fixture uses saved storage state instead of logging in each time,
    making it faster than `authenticated_page` for test suites with many tests.

    Note: Requires session-scoped database setup. Use with
    `@pytest.mark.django_db(transaction=True)` and configure
    your test to use session-scoped live_server.

    Usage:
        @pytest.mark.e2e
        @pytest.mark.django_db(transaction=True)
        def test_something(authenticated_page_fast, server_url):
            authenticated_page_fast.goto(f"{server_url}/admin/")
            # Already logged in via storage state
    """
    page = authenticated_browser_context.new_page()
    yield page
    page.close()


def pytest_addoption(parser):
    """Add custom command-line options."""
    group = parser.getgroup("wagtail-scenario-test")
    group.addoption(
        "--gif",
        action="store_true",
        default=False,
        help="Convert recorded videos to GIF format after tests (requires ffmpeg)",
    )
    group.addoption(
        "--gif-fps",
        type=int,
        default=10,
        help="Frames per second for GIF conversion (default: 10)",
    )
    group.addoption(
        "--gif-width",
        type=int,
        default=800,
        help="Width in pixels for GIF conversion (default: 800)",
    )


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


def pytest_sessionfinish(session, exitstatus):
    """Convert videos to GIFs after test session if --gif flag is set."""
    if not session.config.getoption("--gif", default=False):
        return

    from pathlib import Path

    from wagtail_scenario_test.utils.video import (
        convert_all_videos_to_gif,
        is_ffmpeg_available,
    )

    if not is_ffmpeg_available():
        print("\n⚠️  ffmpeg not found - skipping GIF conversion")
        print("   Install ffmpeg to enable automatic GIF conversion")
        return

    # Look for test-results directory (pytest-playwright default)
    results_dir = Path("test-results")
    if not results_dir.exists():
        return

    fps = session.config.getoption("--gif-fps", default=10)
    width = session.config.getoption("--gif-width", default=800)

    print(f"\n🎬 Converting videos to GIF (fps={fps}, width={width})...")

    gifs = convert_all_videos_to_gif(
        results_dir,
        fps=fps,
        width=width,
        delete_originals=False,
    )

    if gifs:
        print(f"✅ Created {len(gifs)} GIF(s):")
        for gif in gifs:
            print(f"   - {gif}")
