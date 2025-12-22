"""
wagtail-scenario-test: E2E scenario testing framework for Wagtail applications.

This package provides:
- Page Object classes for Wagtail admin UI
- Pytest fixtures for authenticated browser sessions
- Factory utilities for test data creation
- BDD support with pytest-bdd (optional)

Usage:
    from wagtail_scenario_test.page_objects import WagtailAdminPage, SnippetAdminPage
    from wagtail_scenario_test.fixtures import authenticated_page

Example:
    def test_create_snippet(authenticated_page, live_server):
        admin = SnippetAdminPage(
            authenticated_page,
            live_server.url,
            app_name="myapp",
            model_name="mymodel"
        )
        admin.create(name="Test Item")
        admin.assert_success_message()
"""

__version__ = "0.1.0"

from wagtail_scenario_test.page_objects import (
    BasePage,
    WagtailAdminPage,
    SnippetAdminPage,
)

__all__ = [
    "__version__",
    "BasePage",
    "WagtailAdminPage",
    "SnippetAdminPage",
]
