---
description: Conduct repository & web research, then create Discussion or Issue
argument-hint: [research-topic]
---

# Research Task: $ARGUMENTS

## Research Process

### 1. Pre-check
- Check if similar topics exist in Issues/Discussions/PRs
- Review related milestones and GitHub Project README

### 2. Codebase Investigation
- Search and analyze related existing implementations
- Identify affected files and modules
- Understand existing patterns and design principles

### 3. Web Research
- Implementation examples from similar projects
- Best practices
- Related technologies and libraries

### 4. Summarize Research Results
Organize in the following format:
- **Current State**: Current codebase situation
- **Problems/Opportunities**: Issues to solve or features to implement
- **Options**: Possible approaches (with pros and cons)
- **Recommendation**: Recommended approach based on research
- **Next Steps**: Specific action items

### 5. Publish Deliverables

Publish in appropriate format based on research results:

**Create Discussion** (when design discussion or decision-making is needed):

Category IDs (TODO: Update after enabling GitHub Discussions):
- Announcements: `<TBD>`
- General: `<TBD>`
- Ideas: `<TBD>`
- Q&A: `<TBD>`

```bash
# TODO: Update repositoryId and categoryId after enabling GitHub Discussions
gh api graphql -f query='
mutation($repositoryId: ID!, $categoryId: ID!, $title: String!, $body: String!) {
  createDiscussion(input: {
    repositoryId: $repositoryId
    categoryId: $categoryId
    title: $title
    body: $body
  }) {
    discussion {
      url
      number
    }
  }
}' -f repositoryId="<TBD>" -f categoryId="<TBD>" -f title="Title" -f body="Body"
```

**Create Issue** (when specific tasks are clear):
```bash
gh issue create --repo kkm-horikawa/wagtail-scenario-test \
  --title "Title" \
  --body "Issue body" \
  --label "appropriate-label"
```

## Notes
- Reference related Issues found during research with links
- Explicitly mark unclear points as "needs confirmation"
- Include rationale for technical decisions
