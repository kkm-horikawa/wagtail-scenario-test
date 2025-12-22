"""Pytest configuration for wagtail-scenario-test tests."""

from unittest.mock import MagicMock, patch

import pytest


@pytest.fixture
def mock_playwright_expect():
    """Mock Playwright's expect function for unit tests."""
    mock_expect = MagicMock()
    mock_assertions = MagicMock()
    mock_expect.return_value = mock_assertions
    with patch("wagtail_scenario_test.page_objects.base.expect", mock_expect):
        with patch(
            "wagtail_scenario_test.page_objects.wagtail_admin.expect", mock_expect
        ):
            yield mock_expect


@pytest.fixture
def mock_page():
    """Create a mock Playwright page for unit testing."""
    from unittest.mock import MagicMock

    page = MagicMock()
    page.url = "http://localhost:8000/admin/"

    # Mock locator chain
    locator = MagicMock()
    locator.count.return_value = 1
    locator.first = locator
    locator.all.return_value = [locator]
    locator.text_content.return_value = "Test Item"
    locator.inner_text.return_value = "Page content"
    page.locator.return_value = locator

    # Mock get_by_* methods
    page.get_by_role.return_value = locator
    page.get_by_label.return_value = locator
    page.get_by_text.return_value = locator
    page.get_by_placeholder.return_value = locator

    # Mock content
    page.content.return_value = "<html><body>Test</body></html>"

    # Mock screenshot
    page.screenshot.return_value = b"fake-screenshot-data"

    return page


@pytest.fixture
def test_url():
    """Return a test base URL for unit tests."""
    return "http://localhost:8000"


# Override pytest-base-url's base_url fixture to avoid conflicts
@pytest.fixture(scope="session")
def base_url():
    """Override pytest-base-url fixture for tests."""
    return None
