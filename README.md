# wagtail-scenario-test

[![PyPI version](https://badge.fury.io/py/wagtail-scenario-test.svg)](https://badge.fury.io/py/wagtail-scenario-test)
[![CI](https://github.com/kkm-horikawa/wagtail-scenario-test/actions/workflows/ci.yml/badge.svg?branch=develop)](https://github.com/kkm-horikawa/wagtail-scenario-test/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/kkm-horikawa/wagtail-scenario-test/graph/badge.svg)](https://codecov.io/gh/kkm-horikawa/wagtail-scenario-test)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Published on Django Packages](https://img.shields.io/badge/Published%20on-Django%20Packages-0c3c26)](https://djangopackages.org/packages/p/wagtail-scenario-test/)

E2E testing framework for Wagtail applications using Playwright.

## Philosophy

Wagtail is an excellent CMS framework built on Django's developer-friendly foundation. The testing ecosystem is equally strong—Django's TestCase, pytest, and browser automation tools like Selenium and Playwright provide everything needed to build robust, well-tested applications.

Unit tests are essential, but they can't catch everything. **The most intuitive way for engineers to verify application behavior is through scenario tests based on real use cases and requirements.** When you can write tests that mirror how users actually interact with your admin interface, you gain confidence that your application works as intended.

However, we discovered a practical barrier: **Writing E2E tests for Wagtail applications requires significant boilerplate.** Setting up authenticated users, navigating the admin interface, manipulating StreamField blocks—implementing these operations for each test consumes more time than writing the actual test logic.

This gap between "wanting scenario tests" and "the cost of writing them" led us to build this library.

wagtail-scenario-test wraps Wagtail admin operations into a simple, fluent API. What once required dozens of lines of Playwright selectors now takes just a few method calls.

**Focus on your scenarios. Let the framework handle the admin.**

## Quick Start

### 1. Install

```bash
pip install wagtail-scenario-test

# Install browser and system dependencies
playwright install --with-deps chromium
```

### 2. Configure pytest

```toml
# pyproject.toml
[tool.pytest.ini_options]
DJANGO_SETTINGS_MODULE = "mysite.settings.dev"
markers = ["e2e: E2E tests using Playwright"]
```

### 3. Write test

```python
# tests/test_e2e.py
import pytest
from wagtail_scenario_test import WagtailAdmin

@pytest.mark.e2e
@pytest.mark.django_db(transaction=True)
def test_admin_login(authenticated_page, server_url):
    admin = WagtailAdmin(authenticated_page, server_url)
    admin.go_to_dashboard()
    assert "/admin/" in authenticated_page.url
```

### 4. Run

```bash
pytest tests/ -m e2e              # Headless
pytest tests/ -m e2e --headed     # With browser
```

## Core API

### WagtailAdmin (Facade)

```python
admin = WagtailAdmin(authenticated_page, server_url)

# Snippets
snippet = admin.snippet("blog.category")
snippet.create(name="Tech")
snippet.assert_success_message()

# Pages
pages = admin.pages()
pages.navigate_to_explorer()
```

### StreamFieldHelper

```python
from wagtail_scenario_test import StreamFieldHelper

sf = StreamFieldHelper(page, "body")

# Add and edit blocks
index = sf.add_block("Heading")
sf.block(index).fill("Hello World")

# StructBlock fields
sf.block(0).struct("title").fill("Welcome")

# Block management
sf.delete_block(1)
sf.move_block_up(1)
```

### PageAdminPage

```python
from wagtail_scenario_test import PageAdminPage

page_admin = PageAdminPage(page, base_url)
page_admin.edit_page(5)
page_admin.publish()
page_admin.visit_live(5)
```

## Fixtures

Fixtures are auto-loaded. No `conftest.py` configuration needed.

| Fixture | Description |
|---------|-------------|
| `authenticated_page` | Playwright page logged into Wagtail admin |
| `server_url` | Base URL of the test server |
| `home_page` | Root page instance |
| `test_page` | Test page under home_page |

### Custom credentials

```python
# conftest.py
@pytest.fixture
def admin_credentials():
    return {"username": "admin", "password": "admin"}
```

## Running Tests

```bash
# Basic
pytest tests/ -m e2e

# Debug mode
pytest tests/ -m e2e --headed --slowmo=500

# Record video
pytest tests/ -m e2e --video=on

# Convert to GIF (requires ffmpeg)
pytest tests/ -m e2e --video=on --gif
```

## Requirements

- Python 3.10+
- Django 4.2+
- Wagtail 5.0+

## License

MIT License
