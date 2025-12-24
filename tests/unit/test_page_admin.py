"""Unit tests for PageAdminPage."""

from wagtail_scenario_test.page_objects.wagtail_admin import PageAdminPage


class TestPageAdminPageNavigation:
    """Tests for PageAdminPage navigation methods."""

    def test_navigate_to_explorer(self, mock_page, test_url):
        """navigate_to_explorer should click Pages button and wait for panel."""
        page_admin = PageAdminPage(mock_page, test_url)

        page_admin.navigate_to_explorer()

        # Should click the Pages button
        mock_page.get_by_role.assert_called_once_with("button", name="Pages")
        mock_page.get_by_role.return_value.click.assert_called_once()

        # Should wait for the explorer panel
        mock_page.locator.assert_called_with(".c-page-explorer")
        mock_page.locator.return_value.wait_for.assert_called_once_with(
            state="visible", timeout=10000
        )

    def test_inherits_from_wagtail_admin_page(self, mock_page, test_url):
        """PageAdminPage should inherit from WagtailAdminPage."""
        page_admin = PageAdminPage(mock_page, test_url)

        # Should have access to WagtailAdminPage methods
        assert hasattr(page_admin, "login")
        assert hasattr(page_admin, "logout")
        assert hasattr(page_admin, "go_to_dashboard")
        assert hasattr(page_admin, "is_logged_in")


class TestPageAdminPageUrls:
    """Tests for PageAdminPage URL methods."""

    def test_add_child_page_url(self, mock_page, test_url):
        """add_child_page_url should return correct URL."""
        page_admin = PageAdminPage(mock_page, test_url)

        url = page_admin.add_child_page_url(
            parent_page_id=1, app_name="testapp", model_name="testpage"
        )

        assert url == "/admin/pages/add/testapp/testpage/1/"

    def test_edit_page_url(self, mock_page, test_url):
        """edit_page_url should return correct URL."""
        page_admin = PageAdminPage(mock_page, test_url)

        url = page_admin.edit_page_url(page_id=42)

        assert url == "/admin/pages/42/edit/"

    def test_delete_page_url(self, mock_page, test_url):
        """delete_page_url should return correct URL."""
        page_admin = PageAdminPage(mock_page, test_url)

        url = page_admin.delete_page_url(page_id=42)

        assert url == "/admin/pages/42/delete/"

    def test_preview_url(self, mock_page, test_url):
        """preview_url should return correct URL."""
        page_admin = PageAdminPage(mock_page, test_url)

        url = page_admin.preview_url(page_id=42)

        assert url == "/admin/pages/42/edit/preview/"


class TestPageAdminPageGetLiveUrl:
    """Tests for PageAdminPage get_live_url method."""

    def test_get_live_url_returns_href(self, mock_page, test_url):
        """get_live_url should return href when status link exists."""
        mock_link = mock_page.locator.return_value
        mock_link.count.return_value = 1
        mock_link.first.get_attribute.return_value = "/my-page/"

        page_admin = PageAdminPage(mock_page, test_url)
        url = page_admin.get_live_url()

        mock_page.locator.assert_called_with("a.page-status-tag[href]")
        assert url == "/my-page/"

    def test_get_live_url_returns_none_when_not_found(self, mock_page, test_url):
        """get_live_url should return None when status link not found."""
        mock_link = mock_page.locator.return_value
        mock_link.count.return_value = 0

        page_admin = PageAdminPage(mock_page, test_url)
        url = page_admin.get_live_url()

        assert url is None


class TestPageAdminPageEditPage:
    """Tests for PageAdminPage edit_page method."""

    def test_edit_page_navigates_to_edit_url(self, mock_page, test_url):
        """edit_page should navigate to the edit URL."""
        page_admin = PageAdminPage(mock_page, test_url)

        page_admin.edit_page(page_id=5)

        mock_page.goto.assert_called_with(f"{test_url}/admin/pages/5/edit/")

    def test_edit_page_waits_for_navigation(self, mock_page, test_url):
        """edit_page should wait for navigation to complete."""
        page_admin = PageAdminPage(mock_page, test_url)

        page_admin.edit_page(page_id=10)

        # Should call wait_for_load_state (from wait_for_navigation)
        mock_page.wait_for_load_state.assert_called()


class TestPageAdminPageVisitPreview:
    """Tests for PageAdminPage visit_preview method."""

    def test_visit_preview_navigates_to_preview_url(self, mock_page, test_url):
        """visit_preview should navigate to the preview URL."""
        page_admin = PageAdminPage(mock_page, test_url)

        page_admin.visit_preview(page_id=5)

        mock_page.goto.assert_called_with(f"{test_url}/admin/pages/5/edit/preview/")

    def test_visit_preview_waits_for_navigation(self, mock_page, test_url):
        """visit_preview should wait for navigation to complete."""
        page_admin = PageAdminPage(mock_page, test_url)

        page_admin.visit_preview(page_id=10)

        mock_page.wait_for_load_state.assert_called()


class TestPageAdminPageVisitLive:
    """Tests for PageAdminPage visit_live method."""

    def test_visit_live_navigates_to_live_url(self, mock_page, test_url):
        """visit_live should navigate to the live URL."""
        mock_link = mock_page.locator.return_value
        mock_link.count.return_value = 1
        mock_link.first.get_attribute.return_value = "/my-page/"

        page_admin = PageAdminPage(mock_page, test_url)

        page_admin.visit_live(page_id=5)

        # Should first navigate to edit page
        mock_page.goto.assert_any_call(f"{test_url}/admin/pages/5/edit/")
        # Then navigate to live URL
        mock_page.goto.assert_called_with(f"{test_url}/my-page/")

    def test_visit_live_raises_error_when_not_published(self, mock_page, test_url):
        """visit_live should raise ValueError when page has no live URL."""
        import pytest

        mock_link = mock_page.locator.return_value
        mock_link.count.return_value = 0

        page_admin = PageAdminPage(mock_page, test_url)

        with pytest.raises(ValueError, match="not published or has no routable URL"):
            page_admin.visit_live(page_id=5)


class TestPageAdminPagePublish:
    """Tests for PageAdminPage publish method."""

    def test_publish_with_page_id(self, mock_page, test_url):
        """publish with page_id should navigate to edit page and click Publish."""
        page_admin = PageAdminPage(mock_page, test_url)

        page_admin.publish(page_id=5)

        # Should navigate to edit page first
        mock_page.goto.assert_called_with(f"{test_url}/admin/pages/5/edit/")

        # Should open "More actions" dropdown and click Publish button
        mock_page.get_by_role.assert_any_call("button", name="More actions")
        mock_page.get_by_role.assert_any_call("button", name="Publish")

    def test_publish_without_page_id(self, mock_page, test_url):
        """publish without page_id should not navigate, just click Publish."""
        page_admin = PageAdminPage(mock_page, test_url)

        page_admin.publish()

        # Should NOT navigate (no goto call for edit page)
        for call in mock_page.goto.call_args_list:
            assert "/edit/" not in str(call)

        # Should open "More actions" dropdown and click Publish button
        mock_page.get_by_role.assert_any_call("button", name="More actions")
        mock_page.get_by_role.assert_any_call("button", name="Publish")

    def test_publish_waits_for_navigation(self, mock_page, test_url):
        """publish should wait for navigation to complete."""
        page_admin = PageAdminPage(mock_page, test_url)

        page_admin.publish(page_id=10)

        # Should call wait_for_load_state (from wait_for_navigation)
        mock_page.wait_for_load_state.assert_called()


class TestPageAdminPageUnpublish:
    """Tests for PageAdminPage unpublish method."""

    def test_unpublish_with_page_id_and_confirm(self, mock_page, test_url):
        """unpublish with page_id should navigate, open dropdown, and confirm."""
        page_admin = PageAdminPage(mock_page, test_url)

        page_admin.unpublish(page_id=5)

        # Should navigate to edit page first
        mock_page.goto.assert_called_with(f"{test_url}/admin/pages/5/edit/")

        # Should open "Actions" dropdown (exact match)
        mock_page.get_by_role.assert_any_call("button", name="Actions", exact=True)

        # Should click Unpublish link and Yes, unpublish button
        mock_page.get_by_role.assert_any_call("link", name="Unpublish", exact=True)
        mock_page.get_by_role.assert_any_call("button", name="Yes, unpublish")

    def test_unpublish_without_page_id(self, mock_page, test_url):
        """unpublish without page_id should not navigate, just unpublish."""
        page_admin = PageAdminPage(mock_page, test_url)

        page_admin.unpublish()

        # Should NOT navigate (no goto call for edit page)
        for call in mock_page.goto.call_args_list:
            assert "/edit/" not in str(call)

        # Should open "Actions" dropdown and click Unpublish link
        mock_page.get_by_role.assert_any_call("button", name="Actions", exact=True)
        mock_page.get_by_role.assert_any_call("link", name="Unpublish", exact=True)

    def test_unpublish_without_confirm(self, mock_page, test_url):
        """unpublish with confirm=False should not click Yes, unpublish."""
        page_admin = PageAdminPage(mock_page, test_url)

        page_admin.unpublish(page_id=5, confirm=False)

        # Should open "Actions" dropdown and click Unpublish link
        mock_page.get_by_role.assert_any_call("button", name="Actions", exact=True)
        mock_page.get_by_role.assert_any_call("link", name="Unpublish", exact=True)

        # Should NOT call Yes, unpublish
        for call in mock_page.get_by_role.call_args_list:
            args, kwargs = call
            if args[0] == "button" and kwargs.get("name") == "Yes, unpublish":
                raise AssertionError("Yes, unpublish should not be clicked")

    def test_unpublish_waits_for_navigation(self, mock_page, test_url):
        """unpublish should wait for navigation to complete."""
        page_admin = PageAdminPage(mock_page, test_url)

        page_admin.unpublish(page_id=10)

        # Should call wait_for_load_state (from wait_for_navigation)
        mock_page.wait_for_load_state.assert_called()


class TestPageAdminPageDeletePage:
    """Tests for PageAdminPage delete_page method."""

    def test_delete_page_with_confirm(self, mock_page, test_url):
        """delete_page should navigate, open dropdown, click Delete, and confirm."""
        page_admin = PageAdminPage(mock_page, test_url)

        page_admin.delete_page(page_id=5)

        # Should navigate to edit page first
        mock_page.goto.assert_called_with(f"{test_url}/admin/pages/5/edit/")

        # Should open "Actions" dropdown (exact match)
        mock_page.get_by_role.assert_any_call("button", name="Actions", exact=True)

        # Should click Delete link and Yes, delete button
        mock_page.get_by_role.assert_any_call("link", name="Delete", exact=True)
        mock_page.get_by_role.assert_any_call("button", name="Yes, delete")

    def test_delete_page_without_confirm(self, mock_page, test_url):
        """delete_page with confirm=False should not click Yes, delete."""
        page_admin = PageAdminPage(mock_page, test_url)

        page_admin.delete_page(page_id=5, confirm=False)

        # Should navigate to edit page
        mock_page.goto.assert_called_with(f"{test_url}/admin/pages/5/edit/")

        # Should open "Actions" dropdown (exact match) and click Delete link
        mock_page.get_by_role.assert_any_call("button", name="Actions", exact=True)
        mock_page.get_by_role.assert_any_call("link", name="Delete", exact=True)

        # Should NOT call Yes, delete
        for call in mock_page.get_by_role.call_args_list:
            args, kwargs = call
            if args[0] == "button" and kwargs.get("name") == "Yes, delete":
                raise AssertionError("Yes, delete should not be clicked")


class TestPageAdminPageCreateChildPage:
    """Tests for PageAdminPage create_child_page method."""

    def test_create_child_page_with_title_and_slug(self, mock_page, test_url):
        """create_child_page should navigate, fill title/slug, and save draft."""
        page_admin = PageAdminPage(mock_page, test_url)

        page_admin.create_child_page(
            parent_page_id=1,
            page_type="testapp.TestPage",
            title="My Test Page",
            slug="my-test-page",
        )

        # Should navigate to add page URL
        mock_page.goto.assert_called_with(
            f"{test_url}/admin/pages/add/testapp/testpage/1/"
        )

        # Should fill title
        mock_page.locator.assert_any_call("#id_title")

        # Should click Promote tab and fill slug
        mock_page.get_by_role.assert_any_call("tab", name="Promote")
        mock_page.locator.assert_any_call("#id_slug")

        # Should click Save draft (default behavior)
        mock_page.get_by_role.assert_any_call("button", name="Save draft")

    def test_create_child_page_generates_slug_from_title(self, mock_page, test_url):
        """create_child_page should generate slug from title if not provided."""
        page_admin = PageAdminPage(mock_page, test_url)

        page_admin.create_child_page(
            parent_page_id=1,
            page_type="testapp.TestPage",
            title="My Test Page",
        )

        # Should fill slug field (auto-generated)
        mock_page.locator.assert_any_call("#id_slug")

    def test_create_child_page_with_publish(self, mock_page, test_url):
        """create_child_page with publish=True should click Publish."""
        page_admin = PageAdminPage(mock_page, test_url)

        page_admin.create_child_page(
            parent_page_id=1,
            page_type="testapp.TestPage",
            title="Published Page",
            slug="published-page",
            publish=True,
        )

        # Should click Publish button
        mock_page.get_by_role.assert_any_call("button", name="Publish")

    def test_create_child_page_without_save(self, mock_page, test_url):
        """create_child_page with save=False should not click any save button."""
        page_admin = PageAdminPage(mock_page, test_url)

        page_admin.create_child_page(
            parent_page_id=1,
            page_type="testapp.TestPage",
            title="Unsaved Page",
            save=False,
        )

        # Should still click Promote tab (to fill slug)
        mock_page.get_by_role.assert_any_call("tab", name="Promote")

        # Should NOT click any save button
        for call in mock_page.get_by_role.call_args_list:
            args, kwargs = call
            if args[0] == "button":
                assert kwargs.get("name") not in ["Save draft", "Publish"]

    def test_create_child_page_with_additional_fields(self, mock_page, test_url):
        """create_child_page should fill additional fields."""
        page_admin = PageAdminPage(mock_page, test_url)

        page_admin.create_child_page(
            parent_page_id=1,
            page_type="testapp.TestPage",
            title="Page with Fields",
            slug="page-with-fields",
            id_subtitle="A subtitle",
            id_body="Page body content",
        )

        # Should fill additional fields
        mock_page.locator.assert_any_call("#id_subtitle")
        mock_page.locator.assert_any_call("#id_body")

    def test_create_child_page_parses_page_type(self, mock_page, test_url):
        """create_child_page should parse page_type correctly."""
        page_admin = PageAdminPage(mock_page, test_url)

        page_admin.create_child_page(
            parent_page_id=42,
            page_type="myapp.MyCustomPage",
            title="Custom Page",
            slug="custom-page",
        )

        # Should convert model name to lowercase in URL
        mock_page.goto.assert_called_with(
            f"{test_url}/admin/pages/add/myapp/mycustompage/42/"
        )

    def test_create_child_page_handles_field_with_hash_prefix(
        self, mock_page, test_url
    ):
        """create_child_page should handle field IDs with # prefix."""
        page_admin = PageAdminPage(mock_page, test_url)

        page_admin.create_child_page(
            parent_page_id=1,
            page_type="testapp.TestPage",
            title="Test",
            slug="test",
            **{"#id_subtitle": "With hash prefix"},
        )

        # Should use the field ID as-is when it has # prefix
        mock_page.locator.assert_any_call("#id_subtitle")


class TestPageAdminPageGenerateSlug:
    """Tests for PageAdminPage._generate_slug method."""

    def test_generate_slug_basic(self, mock_page, test_url):
        """_generate_slug should convert title to lowercase with hyphens."""
        page_admin = PageAdminPage(mock_page, test_url)

        assert page_admin._generate_slug("My Test Page") == "my-test-page"

    def test_generate_slug_removes_special_chars(self, mock_page, test_url):
        """_generate_slug should remove special characters."""
        page_admin = PageAdminPage(mock_page, test_url)

        assert page_admin._generate_slug("Hello, World!") == "hello-world"

    def test_generate_slug_handles_multiple_spaces(self, mock_page, test_url):
        """_generate_slug should handle multiple spaces."""
        page_admin = PageAdminPage(mock_page, test_url)

        assert page_admin._generate_slug("Hello   World") == "hello-world"

    def test_generate_slug_handles_underscores(self, mock_page, test_url):
        """_generate_slug should convert underscores to hyphens."""
        page_admin = PageAdminPage(mock_page, test_url)

        assert page_admin._generate_slug("hello_world") == "hello-world"


class TestPageAdminPageStreamfield:
    """Tests for PageAdminPage streamfield method."""

    def test_streamfield_returns_helper(self, mock_page, test_url):
        """streamfield should return a StreamFieldHelper instance."""
        from wagtail_scenario_test.page_objects.wagtail_admin import StreamFieldHelper

        page_admin = PageAdminPage(mock_page, test_url)
        sf = page_admin.streamfield("body")

        assert isinstance(sf, StreamFieldHelper)

    def test_streamfield_default_field_name(self, mock_page, test_url):
        """streamfield should use 'body' as default field name."""
        page_admin = PageAdminPage(mock_page, test_url)
        sf = page_admin.streamfield()

        assert sf.field_name == "body"

    def test_streamfield_with_custom_field_name(self, mock_page, test_url):
        """streamfield should accept custom field name."""
        page_admin = PageAdminPage(mock_page, test_url)
        sf = page_admin.streamfield("content")

        assert sf.field_name == "content"

    def test_streamfield_uses_same_page(self, mock_page, test_url):
        """streamfield should pass the same Playwright page to helper."""
        page_admin = PageAdminPage(mock_page, test_url)
        sf = page_admin.streamfield("body")

        assert sf.page is mock_page
