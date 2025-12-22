---
description: Check if an Issue is atomic (single PR scope) and split into sub-issues if needed
argument-hint: [issue-number]
---

# Atomic Check for Issue #$ARGUMENTS

## Purpose

Verify whether the Issue can be completed in a single PR. If not, split it into smaller, atomic sub-issues.

## Phase 1: Issue Information Gathering

### 1.1 View Target Issue
```bash
gh issue view $ARGUMENTS --repo kkm-horikawa/wagtail-scenario-test
```

### 1.2 Check Existing Relationships
```bash
# Check parent Issue
gh api graphql -H "GraphQL-Features: sub_issues" -f query='
query($owner: String!, $repo: String!, $number: Int!) {
  repository(owner: $owner, name: $repo) {
    issue(number: $number) {
      parentIssue { number title state }
    }
  }
}' -f owner="kkm-horikawa" -f repo="wagtail-scenario-test" -F number=$ARGUMENTS

# Check child Issues
gh api graphql -H "GraphQL-Features: sub_issues" -f query='
query($owner: String!, $repo: String!, $number: Int!) {
  repository(owner: $owner, name: $repo) {
    issue(number: $number) {
      subIssues(first: 20) {
        nodes { number title state }
      }
    }
  }
}' -f owner="kkm-horikawa" -f repo="wagtail-scenario-test" -F number=$ARGUMENTS
```

## Phase 2: Atomic Assessment

### 2.1 Atomic Issue Criteria
An Issue is atomic if ALL of the following are true:
- [ ] Single responsibility/purpose
- [ ] Can be completed in ONE PR
- [ ] Independently testable
- [ ] Reasonable change size (guideline: ~500 lines or less)
- [ ] No internal dependencies requiring sequential work

### 2.2 Split Criteria (if not atomic)
Consider splitting by:
- **Feature units**: Independent features as separate issues
- **Layer units**: Model → API → UI
- **Dependency order**: Prerequisites as prior issues

## Phase 3: Create Sub-Issues (if split needed)

### 3.1 Create Child Issue
```bash
gh issue create --repo kkm-horikawa/wagtail-scenario-test \
  --title "[Task] Title" \
  --body "$(cat <<'EOF'
## Parent Issue
Child of #$ARGUMENTS

## Overview
(What this Issue accomplishes)

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Technical Notes
(Implementation guidance if any)
EOF
)" \
  --label "type:task"
```

### 3.2 Set Sub-Issue Relationship
```bash
PARENT_ID=$(gh issue view $ARGUMENTS --repo kkm-horikawa/wagtail-scenario-test --json id --jq ".id")
CHILD_ID=$(gh issue view [child-issue-number] --repo kkm-horikawa/wagtail-scenario-test --json id --jq ".id")

gh api graphql -H "GraphQL-Features: sub_issues" -f query='
mutation($parentId: ID!, $childId: ID!) {
  addSubIssue(input: { issueId: $parentId, subIssueId: $childId }) {
    issue { title number }
    subIssue { title number }
  }
}' -f parentId="$PARENT_ID" -f childId="$CHILD_ID"
```

### 3.3 Set Dependency (Blocked By) if needed
When child issues have dependencies:
```bash
ISSUE_ID=$(gh issue view [dependent-issue] --repo kkm-horikawa/wagtail-scenario-test --json id --jq ".id")
BLOCKING_ID=$(gh issue view [blocking-issue] --repo kkm-horikawa/wagtail-scenario-test --json id --jq ".id")

gh api graphql -H "GraphQL-Features: issue_types" -f query='
mutation($issueId: ID!, $blockingIssueId: ID!) {
  addBlockedBy(input: { issueId: $issueId, blockingIssueId: $blockingIssueId }) {
    issue { title number }
    blockingIssue { title number }
  }
}' -f issueId="$ISSUE_ID" -f blockingIssueId="$BLOCKING_ID"
```

## Phase 4: Post Results

### 4.1 If Atomic (no split needed)
```bash
gh issue comment $ARGUMENTS --repo kkm-horikawa/wagtail-scenario-test --body "$(cat <<'EOF'
## Atomic Check: PASSED

This Issue is atomic and can be completed in a single PR.

- Single responsibility: YES
- Reasonable scope: YES
- Independently testable: YES

---
*Ready for implementation: `/implement $ARGUMENTS`*
EOF
)"
```

### 4.2 If Split Required
```bash
gh issue comment $ARGUMENTS --repo kkm-horikawa/wagtail-scenario-test --body "$(cat <<'EOF'
## Atomic Check: SPLIT COMPLETED

This Issue has been split into the following sub-issues:

### Sub-Issues
- #xxx: Title
- #xxx: Title
- #xxx: Title

### Dependencies
- #xxx blocked by #xxx (must complete first)

### Recommended Order
1. #xxx - (reason)
2. #xxx - (reason)
3. #xxx - (reason)

---
*Proceed with sub-issues in order.*
EOF
)"
```

## Checklist

- [ ] Issue content reviewed
- [ ] Atomic criteria evaluated
- [ ] Decision made (atomic or split)
- [ ] Sub-issues created (if needed)
- [ ] Parent-child relationships set (if needed)
- [ ] Dependencies set (if needed)
- [ ] Result comment posted
