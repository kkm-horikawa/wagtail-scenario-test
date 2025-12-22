---
description: Feasibility check for an Issue - Research official docs, Wagtail internals, and best practices
argument-hint: [issue-number]
---

# Feasibility Check for Issue #$ARGUMENTS

## Purpose

Thoroughly investigate official documentation, Wagtail core implementation, and best practices to:
1. Validate the Issue's proposed approach is sound
2. Identify specific implementation details (imports, patterns, APIs to use)
3. Propose alternatives if the current approach is problematic or infeasible

## Phase 1: Issue Information Gathering

### 1.1 View Target Issue
```bash
gh issue view $ARGUMENTS --repo kkm-horikawa/wagtail-scenario-test
```

### 1.2 Check Parent/Child Relationships
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

## Phase 2: Research & Investigation

### 2.1 Official Documentation Research
- **Wagtail Official Docs**: https://docs.wagtail.org/
- **Django Official Docs**: https://docs.djangoproject.com/
- Search for relevant features, APIs, and recommended patterns
- Note any version-specific considerations

### 2.2 Wagtail Core Implementation Analysis
- Examine how Wagtail implements similar features internally
- Identify reusable base classes, mixins, and utilities
- Find correct import paths and module structures
- Study existing patterns in wagtail.contrib modules

### 2.3 Best Practices Research
- Search for community best practices
- Review well-maintained Wagtail packages for patterns
- Check for known pitfalls or deprecated approaches
- Identify recommended testing strategies

### 2.4 Research Checklist
- [ ] Official Wagtail documentation reviewed
- [ ] Relevant Django documentation reviewed
- [ ] Wagtail core source code examined
- [ ] Similar implementations in ecosystem studied
- [ ] Version compatibility confirmed

## Phase 3: Feasibility Assessment

### 3.1 Assessment Criteria
| Criteria | Status | Notes |
|----------|--------|-------|
| Technically feasible | OK/NG/NEEDS_RESEARCH | |
| Aligns with Wagtail patterns | OK/NG/NEEDS_RESEARCH | |
| No deprecated APIs used | OK/NG/NEEDS_RESEARCH | |
| Compatible with target versions | OK/NG/NEEDS_RESEARCH | |

### 3.2 Key Findings to Document
- **Import paths**: Exact modules and classes to import
- **Base classes/Mixins**: Which to inherit from
- **API patterns**: How to properly integrate with Wagtail
- **Testing approach**: How similar features are tested in Wagtail

## Phase 4: Post Comment to Issue

### 4.1 If Approach is Valid (Typical Case)
Post research findings and confirmation:

```bash
gh issue comment $ARGUMENTS --repo kkm-horikawa/wagtail-scenario-test --body "$(cat <<'EOF'
## Feasibility Check: PASSED ✅

### Research Summary

#### Official Documentation
- (Key findings from official docs)

#### Wagtail Core Implementation Analysis
- (Relevant patterns found in Wagtail source)
- (Import paths to use)

#### Best Practices
- (Recommended approaches)

### Implementation Notes

**Imports:**
```python
from wagtail.xxx import Xxx
```

**Recommended Pattern:**
- (Specific implementation guidance)

### Conclusion
The proposed approach in this Issue is sound and aligns with Wagtail best practices. Ready for implementation.

---
*Next step: `/implement $ARGUMENTS`*
EOF
)"
```

### 4.2 If Approach Needs Adjustment
Post findings with recommendations:

```bash
gh issue comment $ARGUMENTS --repo kkm-horikawa/wagtail-scenario-test --body "$(cat <<'EOF'
## Feasibility Check: ADJUSTMENT RECOMMENDED ⚠️

### Research Summary
(Research findings)

### Issue with Current Approach
- (Explain why the current approach is problematic)

### Recommended Alternative
- (Propose better approach with rationale)

### Implementation Notes
(Specific guidance for the recommended approach)

---
*Please review the recommended changes before proceeding.*
EOF
)"
```

### 4.3 If Infeasible
Post findings with alternatives:

```bash
gh issue comment $ARGUMENTS --repo kkm-horikawa/wagtail-scenario-test --body "$(cat <<'EOF'
## Feasibility Check: NOT FEASIBLE ❌

### Research Summary
(Research findings)

### Why Current Approach is Infeasible
- (Technical reasons)

### Alternative Approaches

#### Option A: (Name)
- **Approach**: (Description)
- **Pros**: (Benefits)
- **Cons**: (Drawbacks)

#### Option B: (Name)
- **Approach**: (Description)
- **Pros**: (Benefits)
- **Cons**: (Drawbacks)

### Recommendation
(Which alternative is recommended and why)

---
*Awaiting decision on how to proceed.*
EOF
)"
```

## Checklist

- [ ] Issue content understood
- [ ] Official documentation researched
- [ ] Wagtail core implementation analyzed
- [ ] Best practices identified
- [ ] Feasibility assessment completed
- [ ] Comment posted to Issue with findings
