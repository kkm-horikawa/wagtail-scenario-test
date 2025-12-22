---
description: Create implementation plan from Issue number, then Draft PR creation → Implementation → Tests → PR open
argument-hint: [issue-number]
---

# Implementation for Issue #$ARGUMENTS

## Phase 1: Information Gathering

### 1.1 Review Issue Content
```bash
gh issue view $ARGUMENTS --repo kkm-horikawa/wagtail-scenario-test
```

### 1.2 Check Parent/Child Relationships and Dependencies
Check sub-issues (child Issues):
```bash
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

Check parent Issue (if this Issue is a child):
```bash
gh api graphql -H "GraphQL-Features: sub_issues" -f query='
query($owner: String!, $repo: String!, $number: Int!) {
  repository(owner: $owner, name: $repo) {
    issue(number: $number) {
      parentIssue { number title }
    }
  }
}' -f owner="kkm-horikawa" -f repo="wagtail-scenario-test" -F number=$ARGUMENTS
```

### 1.3 Review Milestone and Project README
- Check the milestone this Issue belongs to
- Review overall direction in GitHub Project README

### 1.4 Investigate Related Files and Existing Implementation
- Identify affected files
- Understand existing patterns and design principles
- Review development guidelines in CLAUDE.md

## Phase 2: Implementation Plan

### 2.1 Create Plan
Create an implementation plan including:
- **Objective**: What to achieve
- **Files to Change**: New/modified files list
- **Implementation Steps**: Ordered work items
- **Testing Strategy**: What and how to test
- **Risks and Considerations**: Impact on existing features, etc.

## Phase 3: Create Draft PR

### 3.1 Create Branch
```bash
git checkout -b feature/$ARGUMENTS-<description>
```

### 3.2 Create Draft PR
```bash
gh pr create --draft --title "WIP: #$ARGUMENTS Title" --body "$(cat <<'EOF'
## Related Issue
Closes #$ARGUMENTS

## Summary
Changes based on implementation plan

## Changes
- [ ] Work item 1
- [ ] Work item 2

## Testing
- [ ] Unit tests
- [ ] Integration tests

---
Draft PR - Implementation in progress
EOF
)"
```

## Phase 4: Implementation

### 4.1 Coding
- Follow guidelines in CONTRIBUTING.md
- Measure and maintain/improve coverage

### 4.2 Commit Frequently
```bash
git add <files>
git commit -m "feat/fix: change description"
```

## Phase 5: Open PR

### 5.1 Remove Draft Status
Once all tests pass, remove draft status:
```bash
gh pr ready
```

### 5.2 Update PR Body
```bash
gh pr edit --body "$(cat <<'EOF'
## Related Issue
Closes #$ARGUMENTS

## Summary
(Description of implementation)

## Changes
- Change 1
- Change 2

## Testing
- [x] Unit tests passed
- [x] Type check passed
- [x] Lint passed
- [x] Build successful
EOF
)"
```

## Notes
- If dependent Issues are incomplete, implement those first
- Commit large changes incrementally
- If unclear, comment on the Issue to confirm
