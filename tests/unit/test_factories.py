"""Tests for factory classes."""

import pytest
from django.contrib.auth import get_user_model

from wagtail_scenario_test.utils.factories import (
    WagtailSuperUserFactory,
    WagtailUserFactory,
)

User = get_user_model()


@pytest.mark.django_db
class TestWagtailUserFactory:
    """Tests for WagtailUserFactory."""

    def test_creates_user(self):
        """WagtailUserFactory should create a user."""
        user = WagtailUserFactory()

        assert user.pk is not None
        assert user.username.startswith("user")

    def test_creates_with_custom_username(self):
        """WagtailUserFactory should accept custom username."""
        user = WagtailUserFactory(username="custom_user")

        assert user.username == "custom_user"

    def test_sets_email_from_username(self):
        """WagtailUserFactory should set email based on username."""
        user = WagtailUserFactory(username="testuser")

        assert user.email == "testuser@example.com"

    def test_sets_password(self):
        """WagtailUserFactory should set password."""
        user = WagtailUserFactory()

        assert user.check_password("password123")

    def test_user_is_active(self):
        """WagtailUserFactory should create active user."""
        user = WagtailUserFactory()

        assert user.is_active is True

    def test_user_is_not_staff(self):
        """WagtailUserFactory should create non-staff user."""
        user = WagtailUserFactory()

        assert user.is_staff is False

    def test_user_is_not_superuser(self):
        """WagtailUserFactory should create non-superuser."""
        user = WagtailUserFactory()

        assert user.is_superuser is False

    def test_get_or_create_by_username(self):
        """WagtailUserFactory should get or create by username."""
        user1 = WagtailUserFactory(username="same_user")
        user2 = WagtailUserFactory(username="same_user")

        assert user1.pk == user2.pk

    def test_unique_usernames_by_sequence(self):
        """WagtailUserFactory should create unique usernames."""
        user1 = WagtailUserFactory()
        user2 = WagtailUserFactory()

        assert user1.username != user2.username


@pytest.mark.django_db
class TestWagtailSuperUserFactory:
    """Tests for WagtailSuperUserFactory."""

    def test_creates_superuser(self):
        """WagtailSuperUserFactory should create a superuser."""
        admin = WagtailSuperUserFactory()

        assert admin.pk is not None
        assert admin.is_superuser is True

    def test_creates_with_custom_username(self):
        """WagtailSuperUserFactory should accept custom username."""
        admin = WagtailSuperUserFactory(username="custom_admin")

        assert admin.username == "custom_admin"

    def test_user_is_staff(self):
        """WagtailSuperUserFactory should create staff user."""
        admin = WagtailSuperUserFactory()

        assert admin.is_staff is True

    def test_username_prefix_is_admin(self):
        """WagtailSuperUserFactory should use admin prefix."""
        admin = WagtailSuperUserFactory()

        assert admin.username.startswith("admin")

    def test_inherits_password_setting(self):
        """WagtailSuperUserFactory should inherit password behavior."""
        admin = WagtailSuperUserFactory()

        assert admin.check_password("password123")

    def test_inherits_email_generation(self):
        """WagtailSuperUserFactory should inherit email generation."""
        admin = WagtailSuperUserFactory(username="myadmin")

        assert admin.email == "myadmin@example.com"
