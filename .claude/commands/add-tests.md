---
description: Add tests to Draft PR linked to Issue number, then run, fix, and update PR body
argument-hint: [issue-number]
---

# Add Tests for Issue #$ARGUMENTS

## Phase 1: Information Gathering

### 1.1 Review Issue Content
```bash
gh issue view $ARGUMENTS --repo kkm-horikawa/wagtail-scenario-test
```

### 1.2 Check Related PRs
```bash
gh pr list --search "head:feature/$ARGUMENTS" --repo kkm-horikawa/wagtail-scenario-test
```

Or:
```bash
gh pr list --search "#$ARGUMENTS" --repo kkm-horikawa/wagtail-scenario-test
```

### 1.3 Review Milestone and Project README
- Check business requirements in GitHub Project README
- Review requirements from related Issues
- Understand user stories and acceptance criteria

### 1.4 Review Existing Implementation
Check PR changes:
```bash
gh pr diff <pr-number>
```

## Phase 2: Test Case Design

### 2.1 Happy Path (Normal Cases)
- Basic success scenarios
- Main use cases
- Expected normal inputs/outputs

### 2.2 Edge Cases
- Boundary values (minimum, maximum, empty, null)
- Invalid inputs (wrong types, out-of-range values)
- Concurrent execution, race conditions
- Permission boundaries (unauthenticated, insufficient permissions)
- Data dependencies (non-existent ID, deleted data)

### 2.3 Create Test Case Matrix
| Case | Input | Expected Result | Category |
|------|-------|-----------------|----------|
| Normal 1 | ... | ... | Happy path |
| Boundary 1 | ... | ... | Edge case |
| Error 1 | ... | ... | Error handling |

## Phase 3: Test Implementation

### 3.1 Backend Tests (pytest)
Test file placement:
- `tests/test_<module>.py`

```python
import pytest

class TestFeatureName:
    def test_happy_path_description(self, db):
        """Normal case: description"""
        pass

    def test_edge_case_description(self, db):
        """Edge case: description"""
        pass
```

## Phase 4: Test Execution and Fixes

### 4.1 Run Backend Tests
```bash
uv run pytest -v --tb=short
uv run pytest tests/path/to/test_file.py -v  # Specific file
uv run pytest -k "test_name" -v              # Specific test
```

### 4.2 Fix Cycle on Failure
1. Review error messages
2. Fix implementation or test
3. Re-run
4. Repeat until all tests pass

## Phase 5: Update PR

### 5.1 Commit Tests
```bash
git add <test-files>
git commit -m "test: add tests description"
```

### 5.2 Push
```bash
git push
```

### 5.3 Update PR Body with Test Status
```bash
gh pr edit <pr-number> --body "$(cat <<'EOF'
## Related Issue
Closes #$ARGUMENTS

## Summary
(Description of implementation)

## Test Status

### Backend
- [x] pytest all tests passed
- [x] mypy type check passed
- [x] ruff lint passed

### Test Coverage
| Category | Count | Status |
|----------|-------|--------|
| Happy path | X | Passed |
| Edge cases | X | Passed |
| Error handling | X | Passed |

### Added Tests
- `tests/path/to/test_file.py`
  - `test_happy_path_xxx`
  - `test_edge_case_xxx`
EOF
)"
```

## Notes
- Write tests with the same quality standards as implementation
- Keep mocks to a minimum
- Test names should clearly describe what is being tested
- Do not break existing tests
