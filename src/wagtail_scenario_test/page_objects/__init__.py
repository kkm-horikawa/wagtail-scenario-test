"""
Page Objects for Wagtail admin interface.

These classes abstract the Wagtail admin UI into reusable, maintainable
components. When Wagtail's UI changes, only these classes need updating.
"""

from wagtail_scenario_test.page_objects.base import BasePage
from wagtail_scenario_test.page_objects.wagtail_admin import (
    SnippetAdminPage,
    WagtailAdminPage,
)

__all__ = [
    "BasePage",
    "WagtailAdminPage",
    "SnippetAdminPage",
]
