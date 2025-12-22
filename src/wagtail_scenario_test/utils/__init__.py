"""
Utility classes for Wagtail E2E testing.

Provides factory base classes and helper functions.
"""

from wagtail_scenario_test.utils.factories import (
    WagtailSuperUserFactory,
    WagtailUserFactory,
)

__all__ = [
    "WagtailUserFactory",
    "WagtailSuperUserFactory",
]
