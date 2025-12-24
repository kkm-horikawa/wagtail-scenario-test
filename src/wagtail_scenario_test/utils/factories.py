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
        skip_postgeneration_save = True

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    is_active = True

    @factory.post_generation
    def password(self, create: bool, extracted: str | None, **kwargs: object) -> None:
        """Set password after user creation."""
        password = extracted or "password123"
        self.set_password(password)  # type: ignore[attr-defined]
        if create:
            self.save()  # type: ignore[attr-defined]


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
