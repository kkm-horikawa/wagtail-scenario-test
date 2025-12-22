# wagtail-scenario-test

E2E scenario testing framework for Wagtail applications.

## Features

- **Page Object Pattern**: Maintainable abstractions for Wagtail admin UI
- **Pytest Fixtures**: Ready-to-use fixtures for authenticated browser sessions
- **Factory Support**: Base factories for test data creation

## Installation

```bash
pip install wagtail-scenario-test
```

## Quick Start

### 1. Configure pytest

```python
# conftest.py
pytest_plugins = ["wagtail_scenario_test.fixtures"]
```

Or simply install the package - fixtures are auto-registered via pytest11 entry point.

### 2. Configure Django settings for E2E tests

```python
# tests/settings.py
LANGUAGE_CODE = "en"

WAGTAIL_CONTENT_LANGUAGES = [
    ("en", "English"),
]

# For E2E tests with live_server
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "testserver"]
```

### 3. Write your first E2E test

```python
import pytest
from wagtail_scenario_test import SnippetAdminPage

@pytest.mark.e2e
@pytest.mark.django_db(transaction=True)
def test_create_my_snippet(authenticated_page, server_url):
    """Test creating a snippet through the admin UI."""
    # Create a Page Object for your snippet
    admin = SnippetAdminPage(
        authenticated_page,
        server_url,
        app_name="myapp",
        model_name="mysnippet",
    )

    # Create a new snippet
    admin.create(name="Test Snippet")

    # Assert it was created
    admin.assert_success_message()
    assert admin.item_exists_in_list("Test Snippet")
```

### 4. Run tests

```bash
# Headless (for CI)
pytest tests/e2e/ -v

# With browser visible
pytest tests/e2e/ -v --headed

# With slow motion (for debugging)
pytest tests/e2e/ -v --headed --slowmo=500
```

## Page Objects

### BasePage

Base class with common browser interactions:

```python
from wagtail_scenario_test import BasePage

class MyCustomPage(BasePage):
    def do_something(self):
        self.goto("/my-path/")
        self.click_button("Submit")
        self.assert_visible("Success!")
```

### WagtailAdminPage

General Wagtail admin operations:

```python
from wagtail_scenario_test import WagtailAdminPage

admin = WagtailAdminPage(page, base_url)
admin.login("admin", "password")
admin.go_to_dashboard()
admin.search("my query")
admin.assert_success_message()
```

### SnippetAdminPage

For Wagtail snippets (any model registered with `@register_snippet`):

```python
from wagtail_scenario_test import SnippetAdminPage

# Generic usage
admin = SnippetAdminPage(
    page,
    base_url,
    app_name="myapp",
    model_name="mymodel",
)

# CRUD operations
admin.create(name="New Item")
admin.click_item_in_list("New Item")
admin.save()
admin.delete()

# Assertions
admin.assert_item_created("New Item")
admin.assert_validation_error("This field is required")
```

## Fixtures

All fixtures are automatically available when the package is installed:

| Fixture | Description |
|---------|-------------|
| `server_url` | Base URL of the live test server |
| `wagtail_site` | Creates Wagtail site with root page and locale |
| `admin_credentials` | Default admin credentials (customizable) |
| `admin_user_e2e` | Creates admin user for E2E testing |
| `authenticated_page` | Playwright page logged into Wagtail admin |

### Customizing Credentials

```python
# conftest.py
import pytest

@pytest.fixture
def admin_credentials():
    return {"username": "my_admin", "password": "my_password"}
```

## Extending Page Objects

Create custom Page Objects for your specific snippets:

```python
from wagtail_scenario_test import SnippetAdminPage

class ReusableBlockAdmin(SnippetAdminPage):
    """Page Object for ReusableBlock admin."""

    def __init__(self, page, base_url):
        super().__init__(
            page,
            base_url,
            app_name="wagtail_reusable_blocks",
            model_name="reusableblock",
        )

    def add_html_content(self, html: str):
        """Add HTML content to the block."""
        self.click_button("Insert a block")
        self.click_button("HTML")
        self.page.locator("textarea").fill(html)
```

## Factory Support

Base factories for test data:

```python
from wagtail_scenario_test.utils import WagtailSuperUserFactory

# Create admin user
admin = WagtailSuperUserFactory()

# Custom factory
class MySnippetFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MySnippet

    name = factory.Sequence(lambda n: f"Snippet {n}")
```

## Best Practices

1. **Use Page Objects**: Don't interact with Playwright directly in tests
2. **Create via UI**: For editing tests, create data through the admin UI to avoid transaction isolation issues
3. **Use `transaction=True`**: Required for E2E tests with live_server
4. **Add waits**: Use `wait_for_navigation()` after actions that trigger page loads
5. **Take screenshots on failure**: Use `--screenshot=on` for debugging

## Requirements

- Python 3.10+
- Django 4.2+
- Wagtail 5.0+
- pytest 8.0+
- pytest-django 4.8+
- pytest-playwright 0.6.2+

## License

MIT License
