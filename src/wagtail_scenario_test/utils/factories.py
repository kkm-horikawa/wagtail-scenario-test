"""
Factory Boy factories for Wagtail testing.

These factories provide base classes for creating test data.
Extend these in your own tests to create model-specific factories.

Example:
    from wagtail_scenario_test.utils import WagtailSuperUserFactory

    class MyAdminFactory(WagtailSuperUserFactory):
        username = factory.Sequence(lambda n: f"myadmin{n}")
"""

from __future__ import annotations

import factory
from django.contrib.auth import get_user_model


class WagtailUserFactory(factory.django.DjangoModelFactory):
    """
    Factory for creating regular User instances.

    Note: This creates inactive users by default. For admin users,
    use WagtailSuperUserFactory.

    Example:
        user = WagtailUserFactory()
        user = WagtailUserFactory(username="custom_user")
    """

    class Meta:
        model = get_user_model()
        django_get_or_create = ("username",)

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    password = factory.PostGenerationMethodCall("set_password", "password123")
    is_active = True


class WagtailSuperUserFactory(WagtailUserFactory):
    """
    Factory for creating superuser instances.

    Useful for E2E tests that need admin access.

    Example:
        admin = WagtailSuperUserFactory()
        admin = WagtailSuperUserFactory(username="custom_admin")
    """

    username = factory.Sequence(lambda n: f"admin{n}")
    is_staff = True
    is_superuser = True
