"""Tests for package imports and exports."""


class TestPackageImports:
    """Tests for top-level package imports."""

    def test_import_wagtail_admin_from_top_level(self):
        """WagtailAdmin should be importable from top level."""
        from wagtail_scenario_test import WagtailAdmin

        assert WagtailAdmin is not None

    def test_import_base_page_from_page_objects(self):
        """BasePage should be importable from page_objects."""
        from wagtail_scenario_test.page_objects import BasePage

        assert BasePage is not None

    def test_import_wagtail_admin_page_from_page_objects(self):
        """WagtailAdminPage should be importable from page_objects."""
        from wagtail_scenario_test.page_objects import WagtailAdminPage

        assert WagtailAdminPage is not None

    def test_import_snippet_admin_page_from_page_objects(self):
        """SnippetAdminPage should be importable from page_objects."""
        from wagtail_scenario_test.page_objects import SnippetAdminPage

        assert SnippetAdminPage is not None

    def test_import_wagtail_admin_from_page_objects(self):
        """WagtailAdmin should be importable from page_objects."""
        from wagtail_scenario_test.page_objects import WagtailAdmin

        assert WagtailAdmin is not None

    def test_all_exports_from_top_level(self):
        """Top-level __all__ should contain expected exports."""
        import wagtail_scenario_test

        assert hasattr(wagtail_scenario_test, "__all__")
        assert "WagtailAdmin" in wagtail_scenario_test.__all__

    def test_all_exports_from_page_objects(self):
        """page_objects __all__ should contain expected exports."""
        from wagtail_scenario_test import page_objects

        assert hasattr(page_objects, "__all__")
        expected = ["BasePage", "WagtailAdminPage", "SnippetAdminPage", "WagtailAdmin"]
        for name in expected:
            assert name in page_objects.__all__


class TestFactoryImports:
    """Tests for factory imports."""

    def test_import_wagtail_user_factory(self):
        """WagtailUserFactory should be importable."""
        from wagtail_scenario_test.utils.factories import WagtailUserFactory

        assert WagtailUserFactory is not None

    def test_import_wagtail_superuser_factory(self):
        """WagtailSuperUserFactory should be importable."""
        from wagtail_scenario_test.utils.factories import WagtailSuperUserFactory

        assert WagtailSuperUserFactory is not None


class TestFixtureImports:
    """Tests for fixture imports."""

    def test_fixtures_module_exists(self):
        """fixtures module should be importable."""
        from wagtail_scenario_test import fixtures

        assert fixtures is not None

    def test_fixtures_has_server_url(self):
        """fixtures should have server_url fixture."""
        from wagtail_scenario_test import fixtures

        assert hasattr(fixtures, "server_url")
        assert callable(fixtures.server_url)

    def test_fixtures_has_admin_credentials(self):
        """fixtures should have admin_credentials fixture."""
        from wagtail_scenario_test import fixtures

        assert hasattr(fixtures, "admin_credentials")
        assert callable(fixtures.admin_credentials)

    def test_fixtures_has_wagtail_site(self):
        """fixtures should have wagtail_site fixture."""
        from wagtail_scenario_test import fixtures

        assert hasattr(fixtures, "wagtail_site")
        assert callable(fixtures.wagtail_site)

    def test_fixtures_has_admin_user_e2e(self):
        """fixtures should have admin_user_e2e fixture."""
        from wagtail_scenario_test import fixtures

        assert hasattr(fixtures, "admin_user_e2e")
        assert callable(fixtures.admin_user_e2e)

    def test_fixtures_has_authenticated_page(self):
        """fixtures should have authenticated_page fixture."""
        from wagtail_scenario_test import fixtures

        assert hasattr(fixtures, "authenticated_page")
        assert callable(fixtures.authenticated_page)

    def test_fixtures_has_pytest_configure(self):
        """fixtures should have pytest_configure hook."""
        from wagtail_scenario_test import fixtures

        assert hasattr(fixtures, "pytest_configure")
        assert callable(fixtures.pytest_configure)
