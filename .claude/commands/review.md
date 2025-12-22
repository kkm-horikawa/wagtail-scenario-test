---
description: Review a PR against its linked Issue and comments for best practices compliance
argument-hint: [pr-number]
---

# Code Review for PR #$ARGUMENTS

## Purpose

Review a Pull Request by:
1. Reading the linked Issue(s) and all comments (including feasibility check results)
2. Checking implementation against Issue requirements and best practices
3. Providing actionable feedback

## Phase 1: Gather Context

### 1.1 View PR Details
```bash
gh pr view $ARGUMENTS --repo kkm-horikawa/wagtail-scenario-test
```

### 1.2 Get Linked Issues
```bash
gh pr view $ARGUMENTS --repo kkm-horikawa/wagtail-scenario-test --json body,title --jq '.body' | grep -oE '#[0-9]+'
```

### 1.3 View PR Diff
```bash
gh pr diff $ARGUMENTS --repo kkm-horikawa/wagtail-scenario-test
```

### 1.4 Read Linked Issue(s) and Comments
For each linked issue:
```bash
gh issue view [issue-number] --repo kkm-horikawa/wagtail-scenario-test
gh issue view [issue-number] --repo kkm-horikawa/wagtail-scenario-test --comments
```

## Phase 2: Review Checklist

### 2.1 Requirements Compliance
- [ ] All acceptance criteria from Issue are met
- [ ] Implementation follows guidance from feasibility check comments
- [ ] No scope creep (only implements what Issue specifies)

### 2.2 Wagtail Best Practices
- [ ] Uses `get_image_model_string()` for image ForeignKeys
- [ ] Uses `gettext_lazy as _` for all user-facing strings
- [ ] Proper use of Wagtail APIs (panels, settings, etc.)
- [ ] Compatible with custom image/document models

### 2.3 Django Best Practices
- [ ] Migrations are correct and minimal
- [ ] No N+1 query issues
- [ ] Proper use of `on_delete` for ForeignKeys
- [ ] Related names are unique or use `"+"`

### 2.4 Code Quality
- [ ] Follows project coding style (ruff compliance)
- [ ] No hardcoded strings that should be translatable
- [ ] Appropriate error handling
- [ ] No security issues (XSS, injection, etc.)

### 2.5 Testing
- [ ] Unit tests cover new functionality
- [ ] Tests are meaningful (not just coverage)
- [ ] Edge cases are tested

### 2.6 Documentation
- [ ] help_text is clear and follows SEO best practices
- [ ] Code comments where logic is non-obvious
- [ ] README updated if needed

## Phase 3: Post Review

### 3.1 If LGTM
```bash
gh pr review $ARGUMENTS --repo kkm-horikawa/wagtail-scenario-test --approve --body "$(cat <<'EOF'
## Review: LGTM ✅

### Summary
(Brief summary of what was reviewed)

### Checklist
- [x] Requirements from Issue met
- [x] Wagtail best practices followed
- [x] Code quality acceptable
- [x] Tests adequate

### Notes
(Any additional observations or minor suggestions)
EOF
)"
```

### 3.2 If Changes Requested
```bash
gh pr review $ARGUMENTS --repo kkm-horikawa/wagtail-scenario-test --request-changes --body "$(cat <<'EOF'
## Review: CHANGES REQUESTED ⚠️

### Summary
(Brief summary of the issues found)

### Required Changes

#### 1. (Issue title)
**Location:** `path/to/file.py:line`
**Problem:** (Description)
**Suggestion:**
```python
# Recommended fix
```

#### 2. (Issue title)
...

### Optional Improvements
- (Nice-to-have suggestions)

### Reference
- Issue requirements: #XX
- Feasibility check: (link to comment if applicable)
EOF
)"
```

### 3.3 If Need More Information
```bash
gh pr comment $ARGUMENTS --repo kkm-horikawa/wagtail-scenario-test --body "$(cat <<'EOF'
## Review: NEEDS CLARIFICATION ❓

### Questions

1. (Question about implementation choice)
2. (Question about edge case handling)

### Context
(Why this clarification is needed)
EOF
)"
```

## Review Focus Areas by Type

### Model Changes
- Field types and options are appropriate
- `get_image_model_string()` / `get_document_model_string()` used
- Proper `related_name` handling
- Migration is clean

### Template Tag Changes
- Context handling is correct
- Graceful fallbacks for missing data
- No XSS vulnerabilities
- Proper use of `mark_safe` only where needed

### Template Changes
- Proper escaping (or intentional `|safe` with justification)
- No hardcoded text (use `{% trans %}` or context)
- Valid HTML structure

### Test Changes
- Tests are independent and repeatable
- Proper use of fixtures/factories
- Assertions are meaningful

## Checklist

- [ ] PR description and linked issues read
- [ ] All issue comments (including feasibility) reviewed
- [ ] Code diff reviewed thoroughly
- [ ] Best practices checklist completed
- [ ] Review posted to PR
