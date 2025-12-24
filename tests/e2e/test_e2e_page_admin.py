"""E2E tests for PageAdminPage."""

import pytest

from wagtail_scenario_test import PageAdminPage


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
class TestPageAdminUnpublishE2E:
    """E2E tests for PageAdminPage.unpublish()."""

    def test_unpublish_live_page(self, authenticated_page, server_url, home_page):
        """Test unpublishing a live page through the admin UI."""
        page_admin = PageAdminPage(authenticated_page, server_url)

        # First create and publish a page
        page_admin.create_child_page(
            parent_page_id=home_page.id,
            page_type="testapp.TestPage",
            title="Page To Unpublish",
            slug="page-to-unpublish",
            publish=True,
        )
        page_admin.assert_success_message()

        # Get the created page ID
        from tests.testapp.models import TestPage

        created_page = TestPage.objects.get(title="Page To Unpublish")
        assert created_page.live  # Should be live initially

        # Unpublish the page
        page_admin.unpublish(page_id=created_page.id)

        # Should show success message
        page_admin.assert_success_message()

        # Verify the page is no longer live
        created_page.refresh_from_db()
        assert not created_page.live

    def test_unpublish_from_edit_page(self, authenticated_page, server_url, home_page):
        """Test unpublishing a page when already on the edit page."""
        page_admin = PageAdminPage(authenticated_page, server_url)

        # First create and publish a page
        page_admin.create_child_page(
            parent_page_id=home_page.id,
            page_type="testapp.TestPage",
            title="Page To Unpublish From Edit",
            slug="page-to-unpublish-from-edit",
            publish=True,
        )
        page_admin.assert_success_message()

        # Get the created page ID
        from tests.testapp.models import TestPage

        created_page = TestPage.objects.get(title="Page To Unpublish From Edit")
        assert created_page.live

        # Navigate to edit page first
        page_admin.edit_page(created_page.id)

        # Then unpublish without passing page_id
        page_admin.unpublish()

        # Should show success message
        page_admin.assert_success_message()

        # Verify the page is no longer live
        created_page.refresh_from_db()
        assert not created_page.live


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


@pytest.mark.e2e
@pytest.mark.django_db(transaction=True)
class TestPageAdminGetLiveUrlE2E:
    """E2E tests for PageAdminPage.get_live_url()."""

    def test_get_live_url_returns_url_for_published_page(
        self, authenticated_page, server_url, home_page
    ):
        """Test get_live_url returns URL for a published page."""
        page_admin = PageAdminPage(authenticated_page, server_url)

        # Create and publish a page
        page_admin.create_child_page(
            parent_page_id=home_page.id,
            page_type="testapp.TestPage",
            title="Published Page For URL",
            slug="published-page-for-url",
            publish=True,
        )
        page_admin.assert_success_message()

        # Get the created page ID
        from tests.testapp.models import TestPage

        created_page = TestPage.objects.get(title="Published Page For URL")

        # Navigate to edit the page
        page_admin.edit_page(created_page.id)

        # Get the live URL
        live_url = page_admin.get_live_url()

        # Should return a URL containing the slug
        assert live_url is not None
        assert "published-page-for-url" in live_url

    def test_get_live_url_returns_none_for_draft_page(
        self, authenticated_page, server_url, home_page
    ):
        """Test get_live_url returns None for a draft (unpublished) page."""
        page_admin = PageAdminPage(authenticated_page, server_url)

        # Create a draft page (not published)
        page_admin.create_child_page(
            parent_page_id=home_page.id,
            page_type="testapp.TestPage",
            title="Draft Page For URL",
            slug="draft-page-for-url",
        )
        page_admin.assert_success_message()

        # Get the created page ID
        from tests.testapp.models import TestPage

        created_page = TestPage.objects.get(title="Draft Page For URL")

        # Navigate to edit the page
        page_admin.edit_page(created_page.id)

        # Get the live URL
        live_url = page_admin.get_live_url()

        # Should return None for unpublished page
        assert live_url is None


@pytest.mark.e2e
@pytest.mark.django_db(transaction=True)
class TestPageAdminVisitPreviewE2E:
    """E2E tests for PageAdminPage.visit_preview()."""

    def test_visit_preview_navigates_to_preview(
        self, authenticated_page, server_url, home_page
    ):
        """Test visit_preview navigates to the preview URL."""
        page_admin = PageAdminPage(authenticated_page, server_url)

        # Create a page
        page_admin.create_child_page(
            parent_page_id=home_page.id,
            page_type="testapp.TestPage",
            title="Page To Preview",
            slug="page-to-preview",
        )
        page_admin.assert_success_message()

        # Get the created page ID
        from tests.testapp.models import TestPage

        created_page = TestPage.objects.get(title="Page To Preview")

        # Visit preview
        page_admin.visit_preview(created_page.id)

        # Should be on the preview URL
        assert f"/admin/pages/{created_page.id}/edit/preview/" in authenticated_page.url


@pytest.mark.e2e
@pytest.mark.django_db(transaction=True)
class TestPageAdminVisitLiveE2E:
    """E2E tests for PageAdminPage.visit_live()."""

    def test_visit_live_navigates_to_live_page(
        self, authenticated_page, server_url, home_page
    ):
        """Test visit_live navigates to the live URL of a published page."""
        page_admin = PageAdminPage(authenticated_page, server_url)

        # Create and publish a page
        page_admin.create_child_page(
            parent_page_id=home_page.id,
            page_type="testapp.TestPage",
            title="Page To Visit Live",
            slug="page-to-visit-live",
            publish=True,
        )
        page_admin.assert_success_message()

        # Get the created page ID
        from tests.testapp.models import TestPage

        created_page = TestPage.objects.get(title="Page To Visit Live")

        # Visit live page
        page_admin.visit_live(created_page.id)

        # Should be on the live URL (contains the slug)
        assert "page-to-visit-live" in authenticated_page.url
        # Should not be in admin
        assert "/admin/" not in authenticated_page.url

    def test_visit_live_raises_error_for_draft_page(
        self, authenticated_page, server_url, home_page
    ):
        """Test visit_live raises ValueError for unpublished page."""
        import pytest as pt

        page_admin = PageAdminPage(authenticated_page, server_url)

        # Create a draft page (not published)
        page_admin.create_child_page(
            parent_page_id=home_page.id,
            page_type="testapp.TestPage",
            title="Draft Page To Visit",
            slug="draft-page-to-visit",
        )
        page_admin.assert_success_message()

        # Get the created page ID
        from tests.testapp.models import TestPage

        created_page = TestPage.objects.get(title="Draft Page To Visit")

        # Should raise ValueError
        with pt.raises(ValueError, match="not published or has no routable URL"):
            page_admin.visit_live(created_page.id)
