"""E2E tests for PageAdminPage."""

import pytest
from wagtail.models import Page

from wagtail_scenario_test import PageAdminPage


@pytest.fixture
def home_page(db, wagtail_site):
    """Get or create a home page under the root page."""
    root = Page.objects.get(depth=1)
    # Check if a page already exists under root
    home = root.get_children().first()
    if home is None:
        # Create a simple home page
        home = Page(title="Home", slug="home")
        root.add_child(instance=home)
    # Make sure the TestPage model is allowed as a child
    # by returning a page that can have TestPage children
    return home


@pytest.fixture
def root_page(db, wagtail_site):
    """Get the root page for creating test pages."""
    return Page.objects.get(depth=1)


@pytest.mark.e2e
@pytest.mark.django_db(transaction=True)
class TestPageAdminE2E:
    """E2E tests for PageAdminPage."""

    def test_navigate_to_explorer(self, authenticated_page, server_url):
        """Test navigating to the page explorer."""
        page_admin = PageAdminPage(authenticated_page, server_url)
        page_admin.go_to_dashboard()

        page_admin.navigate_to_explorer()

        # The explorer panel should be visible
        explorer = authenticated_page.locator(".c-page-explorer")
        assert explorer.is_visible()


@pytest.mark.e2e
@pytest.mark.django_db(transaction=True)
class TestPageAdminCreateChildPageE2E:
    """E2E tests for PageAdminPage.create_child_page()."""

    def test_create_child_page_as_draft(
        self, authenticated_page, server_url, home_page
    ):
        """Test creating a child page as draft."""
        page_admin = PageAdminPage(authenticated_page, server_url)

        page_admin.create_child_page(
            parent_page_id=home_page.id,
            page_type="testapp.TestPage",
            title="E2E Test Page Draft",
            slug="e2e-test-page-draft",
        )

        # Should show success message
        page_admin.assert_success_message()

        # Verify page was created in database
        from tests.testapp.models import TestPage

        assert TestPage.objects.filter(title="E2E Test Page Draft").exists()

        # The page should not be live (draft)
        created_page = TestPage.objects.get(title="E2E Test Page Draft")
        assert not created_page.live

    def test_create_child_page_and_publish(
        self, authenticated_page, server_url, home_page
    ):
        """Test creating a child page and publishing it."""
        page_admin = PageAdminPage(authenticated_page, server_url)

        page_admin.create_child_page(
            parent_page_id=home_page.id,
            page_type="testapp.TestPage",
            title="E2E Test Page Published",
            slug="e2e-test-page-published",
            publish=True,
        )

        # Should show success message
        page_admin.assert_success_message()

        # Verify page was created and is live
        from tests.testapp.models import TestPage

        created_page = TestPage.objects.get(title="E2E Test Page Published")
        assert created_page.live

    def test_create_child_page_with_additional_fields(
        self, authenticated_page, server_url, home_page
    ):
        """Test creating a child page with subtitle and body fields."""
        page_admin = PageAdminPage(authenticated_page, server_url)

        page_admin.create_child_page(
            parent_page_id=home_page.id,
            page_type="testapp.TestPage",
            title="E2E Test Page With Fields",
            slug="e2e-test-page-with-fields",
            id_subtitle="Test Subtitle",
            id_body="Test body content",
        )

        # Should show success message
        page_admin.assert_success_message()

        # Verify fields were saved
        from tests.testapp.models import TestPage

        created_page = TestPage.objects.get(title="E2E Test Page With Fields")
        assert created_page.subtitle == "Test Subtitle"
        assert created_page.body == "Test body content"

    def test_add_child_page_url(self, authenticated_page, server_url):
        """Test that add_child_page_url returns correct URL."""
        page_admin = PageAdminPage(authenticated_page, server_url)

        url = page_admin.add_child_page_url(
            parent_page_id=1,
            app_name="testapp",
            model_name="testpage",
        )

        assert url == "/admin/pages/add/testapp/testpage/1/"


@pytest.mark.e2e
@pytest.mark.django_db(transaction=True)
class TestPageAdminEditPageE2E:
    """E2E tests for PageAdminPage.edit_page()."""

    def test_edit_page_navigates_to_edit_form(
        self, authenticated_page, server_url, home_page
    ):
        """Test navigating to edit an existing page."""
        page_admin = PageAdminPage(authenticated_page, server_url)

        # First create a page to edit
        page_admin.create_child_page(
            parent_page_id=home_page.id,
            page_type="testapp.TestPage",
            title="Page To Edit",
            slug="page-to-edit",
        )
        page_admin.assert_success_message()

        # Get the created page ID
        from tests.testapp.models import TestPage

        created_page = TestPage.objects.get(title="Page To Edit")

        # Navigate to edit the page
        page_admin.edit_page(created_page.id)

        # Should be on the edit page
        assert f"/admin/pages/{created_page.id}/edit/" in authenticated_page.url

        # The title field should be visible and contain the page title
        title_input = authenticated_page.locator("#id_title")
        assert title_input.input_value() == "Page To Edit"

    def test_edit_page_url(self, authenticated_page, server_url):
        """Test that edit_page_url returns correct URL."""
        page_admin = PageAdminPage(authenticated_page, server_url)

        url = page_admin.edit_page_url(page_id=42)

        assert url == "/admin/pages/42/edit/"


@pytest.mark.e2e
@pytest.mark.django_db(transaction=True)
class TestPageAdminPublishE2E:
    """E2E tests for PageAdminPage.publish()."""

    def test_publish_draft_page(self, authenticated_page, server_url, home_page):
        """Test publishing a draft page through the admin UI."""
        page_admin = PageAdminPage(authenticated_page, server_url)

        # First create a page as draft
        page_admin.create_child_page(
            parent_page_id=home_page.id,
            page_type="testapp.TestPage",
            title="Page To Publish",
            slug="page-to-publish",
        )
        page_admin.assert_success_message()

        # Get the created page ID
        from tests.testapp.models import TestPage

        created_page = TestPage.objects.get(title="Page To Publish")
        assert not created_page.live  # Should be draft initially

        # Publish the page
        page_admin.publish(page_id=created_page.id)

        # Should show success message
        page_admin.assert_success_message()

        # Verify the page is now live
        created_page.refresh_from_db()
        assert created_page.live

    def test_publish_from_edit_page(self, authenticated_page, server_url, home_page):
        """Test publishing a page when already on the edit page."""
        page_admin = PageAdminPage(authenticated_page, server_url)

        # First create a page as draft
        page_admin.create_child_page(
            parent_page_id=home_page.id,
            page_type="testapp.TestPage",
            title="Page To Publish From Edit",
            slug="page-to-publish-from-edit",
        )
        page_admin.assert_success_message()

        # Get the created page ID
        from tests.testapp.models import TestPage

        created_page = TestPage.objects.get(title="Page To Publish From Edit")

        # Navigate to edit page first
        page_admin.edit_page(created_page.id)

        # Then publish without passing page_id
        page_admin.publish()

        # Should show success message
        page_admin.assert_success_message()

        # Verify the page is now live
        created_page.refresh_from_db()
        assert created_page.live


@pytest.mark.e2e
@pytest.mark.django_db(transaction=True)
class TestPageAdminDeletePageE2E:
    """E2E tests for PageAdminPage.delete_page()."""

    def test_delete_page_removes_page(self, authenticated_page, server_url, home_page):
        """Test deleting a page through the admin UI.

        This tests the Wagtail 7+ UI where Delete is a link in the
        header dropdown menu, not a direct button.
        """
        page_admin = PageAdminPage(authenticated_page, server_url)

        # First create a page to delete
        page_admin.create_child_page(
            parent_page_id=home_page.id,
            page_type="testapp.TestPage",
            title="Page To Delete",
            slug="page-to-delete",
        )
        page_admin.assert_success_message()

        # Get the created page ID
        from tests.testapp.models import TestPage

        created_page = TestPage.objects.get(title="Page To Delete")
        page_id = created_page.id

        # Delete the page
        page_admin.delete_page(page_id)

        # Should show success message
        page_admin.assert_success_message()

        # Verify the page no longer exists
        assert not TestPage.objects.filter(id=page_id).exists()

    def test_delete_page_url(self, authenticated_page, server_url):
        """Test that delete_page_url returns correct URL."""
        page_admin = PageAdminPage(authenticated_page, server_url)

        url = page_admin.delete_page_url(page_id=42)

        assert url == "/admin/pages/42/delete/"
