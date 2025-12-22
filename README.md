# wagtail-scenario-test

E2E scenario testing framework for Wagtail applications using Playwright.

## Features

- **WagtailAdmin Facade**: Simple, intuitive API for Wagtail admin operations
- **Page Object Pattern**: Maintainable abstractions for Wagtail admin UI
- **Pytest Fixtures**: Ready-to-use fixtures for authenticated browser sessions
- **Factory Support**: Base factories for test data creation

## Installation

```bash
pip install wagtail-scenario-test

# Install Playwright browsers
playwright install
```

## Quick Start

### 1. Write your first E2E test

```python
import pytest
from wagtail_scenario_test import WagtailAdmin

@pytest.mark.e2e
@pytest.mark.django_db(transaction=True)
def test_create_snippet(authenticated_page, server_url):
    """Test creating a snippet through the admin UI."""
    admin = WagtailAdmin(authenticated_page, server_url)

    # Get snippet admin for your model
    snippet = admin.snippet("myapp.mymodel")

    # Create a new snippet
    snippet.create(name="My New Item")

    # Verify success
    snippet.assert_success_message()
    assert snippet.item_exists_in_list("My New Item")
```

### 2. Configure Django settings

```python
# tests/settings.py (or conftest.py)
DJANGO_SETTINGS_MODULE = "tests.settings"

# Required settings
LANGUAGE_CODE = "en"
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "testserver"]

WAGTAIL_CONTENT_LANGUAGES = [("en", "English")]
```

### 3. Run tests

```bash
# Headless (for CI)
pytest tests/ -m e2e

# With browser visible
pytest tests/ -m e2e --headed

# With slow motion (for debugging)
pytest tests/ -m e2e --headed --slowmo=500
```

## WagtailAdmin Facade

The `WagtailAdmin` class is the main entry point for E2E testing:

```python
from wagtail_scenario_test import WagtailAdmin

def test_admin_operations(authenticated_page, server_url):
    admin = WagtailAdmin(authenticated_page, server_url)

    # Navigate
    admin.go_to_dashboard()

    # Search
    admin.global_search("my query")

    # Work with snippets
    snippet = admin.snippet("blog.category")
    snippet.create(name="Technology")

    # Assertions
    admin.assert_success_message()
    admin.assert_success_message(contains="created")
```

### Snippet Operations

```python
snippet = admin.snippet("myapp.mymodel")

# Navigation
snippet.go_to_list()           # Go to list view
snippet.go_to_add()            # Go to add form
snippet.go_to_edit(123)        # Go to edit form for ID 123

# CRUD
snippet.create(name="New Item")              # Create with name field
snippet.create(name="Item", id_slug="item")  # Create with additional fields
snippet.save()                               # Click Save button
snippet.delete()                             # Delete with confirmation

# List operations
count = snippet.get_item_count()             # Count items in list
items = snippet.get_list_items()             # Get all item titles
exists = snippet.item_exists_in_list("Name") # Check if item exists
snippet.click_item_in_list("Name")           # Click to edit

# Assertions
snippet.assert_success_message()
snippet.assert_item_created("New Item")
snippet.assert_validation_error("This field is required")
```

## Fixtures

All fixtures are automatically available when the package is installed:

| Fixture | Scope | Description |
|---------|-------|-------------|
| `authenticated_page` | function | Playwright page logged into Wagtail admin |
| `server_url` | function | Base URL of the live test server |
| `admin_user_e2e` | function | Creates admin user for E2E testing |
| `admin_credentials` | function | Default admin credentials |
| `wagtail_site` | function | Creates Wagtail site with root page |

### Usage Example

```python
@pytest.mark.e2e
@pytest.mark.django_db(transaction=True)
def test_with_fixtures(authenticated_page, server_url):
    # authenticated_page is already logged in
    # server_url is the test server URL (e.g., "http://localhost:12345")
    admin = WagtailAdmin(authenticated_page, server_url)
    admin.go_to_dashboard()
```

### Customizing Credentials

```python
# conftest.py
import pytest

@pytest.fixture
def admin_credentials():
    return {"username": "custom_admin", "password": "custom_password"}
```

## Page Objects

### BasePage

Base class with common browser interactions:

```python
from wagtail_scenario_test.page_objects import BasePage

class MyPage(BasePage):
    def do_something(self):
        self.goto("/my-path/")
        self.click_button("Submit")
        self.wait_for_navigation()
        self.assert_visible("Success!")
```

**Available Methods:**

| Method | Description |
|--------|-------------|
| `goto(path)` | Navigate to path |
| `reload()` | Reload current page |
| `current_path()` | Get current URL path |
| `wait_for_navigation()` | Wait for page load |
| `wait_for_element(selector)` | Wait for element visibility |
| `click_button(name)` | Click button by name |
| `click_link(name)` | Click link by name |
| `fill_field(label, value)` | Fill textbox by label |
| `fill_field_by_id(id, value)` | Fill field by ID |
| `select_option(label, value)` | Select dropdown option |
| `check_checkbox(label)` | Check checkbox |
| `assert_visible(text)` | Assert text is visible |
| `assert_url_contains(path)` | Assert URL contains path |
| `screenshot(name)` | Take screenshot |
| `get_page_content()` | Get page HTML |

### Extending Page Objects

Create custom Page Objects for your specific models:

```python
from wagtail_scenario_test.page_objects import SnippetAdminPage

class CategoryAdmin(SnippetAdminPage):
    """Page Object for Category snippet."""

    def __init__(self, page, base_url):
        super().__init__(
            page, base_url,
            app_name="blog",
            model_name="category",
        )

    def create_with_color(self, name: str, color: str):
        """Create category with color field."""
        self.go_to_add()
        self.page.locator("#id_name").fill(name)
        self.page.locator("#id_color").fill(color)
        self.save()
```

## Factory Support

```python
from wagtail_scenario_test.utils import WagtailUserFactory, WagtailSuperUserFactory

# Create regular user
user = WagtailUserFactory()

# Create superuser
admin = WagtailSuperUserFactory()

# Custom attributes
admin = WagtailSuperUserFactory(username="custom_admin")
```

## Video Recording & GIF Conversion

Record test videos using pytest-playwright's built-in `--video` option and automatically convert them to GIF format for documentation and debugging.

### Record Videos

```bash
# Record videos for failed tests only
pytest tests/ -m e2e --video=retain-on-failure

# Record all test videos
pytest tests/ -m e2e --video=on

# Videos are saved to test-results/ directory
```

### Convert Videos to GIF

Use the `--gif` option to automatically convert recorded videos to GIF format:

```bash
# Record and convert to GIF
pytest tests/ -m e2e --video=on --gif

# Customize GIF quality
pytest tests/ -m e2e --video=on --gif --gif-fps=15 --gif-width=1024
```

**GIF Options:**

| Option | Default | Description |
|--------|---------|-------------|
| `--gif` | off | Enable automatic GIF conversion |
| `--gif-fps` | 10 | Frames per second (lower = smaller file) |
| `--gif-width` | 800 | Width in pixels (height auto-scaled) |

**Requirements:** ffmpeg must be installed for GIF conversion.

```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
apt-get install ffmpeg
```

### Programmatic Conversion

```python
from wagtail_scenario_test.utils import convert_video_to_gif, is_ffmpeg_available

if is_ffmpeg_available():
    gif_path = convert_video_to_gif("test-results/video.webm")
    print(f"Created: {gif_path}")
```

## Best Practices

### 1. Use the Facade

Prefer `WagtailAdmin` facade over direct Page Object usage:

```python
# Good
admin = WagtailAdmin(page, url)
admin.snippet("myapp.mymodel").create(name="Test")

# Avoid (unless extending)
snippet = SnippetAdminPage(page, url, app_name="myapp", model_name="mymodel")
```

### 2. Mark E2E Tests

Always mark E2E tests for selective running:

```python
@pytest.mark.e2e
@pytest.mark.django_db(transaction=True)
def test_something(authenticated_page, server_url):
    ...
```

### 3. Use Headed Mode for Debugging

```bash
# See what's happening
pytest tests/ -m e2e --headed --slowmo=500

# Pause on failure
pytest tests/ -m e2e --headed -x
```

### 4. Create Data via UI

For editing tests, create data through the UI to avoid transaction issues:

```python
def test_edit_snippet(authenticated_page, server_url):
    admin = WagtailAdmin(authenticated_page, server_url)
    snippet = admin.snippet("myapp.mymodel")

    # Create first, then edit
    snippet.create(name="Original Name")
    snippet.click_item_in_list("Original Name")

    # Edit
    snippet.page.locator("#id_name").fill("Updated Name")
    snippet.save()
    snippet.assert_success_message()
```

## Requirements

- Python 3.10+
- Django 4.2+
- Wagtail 5.0+
- pytest 8.0+
- pytest-django 4.8+
- pytest-playwright 0.6.2+

## License

MIT License
