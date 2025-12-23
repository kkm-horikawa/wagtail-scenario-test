"""
wagtail-scenario-test: E2E scenario testing framework for Wagtail applications.

This package provides:
- Page Object classes for Wagtail admin UI
- WagtailAdmin facade for simplified API
- Pytest fixtures for authenticated browser sessions
- Factory utilities for test data creation

Usage:
    from wagtail_scenario_test import WagtailAdmin

Example:
    def test_create_snippet(authenticated_page, server_url):
        admin = WagtailAdmin(authenticated_page, server_url)
        admin.snippet("myapp.mymodel").create(name="Test Item")
        admin.snippet("myapp.mymodel").assert_item_created("Test Item")
"""

__version__ = "0.1.0"

from wagtail_scenario_test.page_objects import (
    BasePage,
    PageAdminPage,
    SnippetAdminPage,
    WagtailAdmin,
    WagtailAdminPage,
)

__all__ = [
    "__version__",
    "BasePage",
    "WagtailAdmin",
    "WagtailAdminPage",
    "SnippetAdminPage",
    "PageAdminPage",
]
