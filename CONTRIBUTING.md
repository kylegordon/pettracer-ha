# Contributing to PetTracer Home Assistant Integration

## Workflow Policy: PRs Only — No Direct Commits to `master`

**All changes must be made via a pull request. Direct commits to `master` are not allowed.**

This applies to everyone — including automated tools and maintainers.

### How Changes Are Made

This repository uses [GitHub Copilot](https://github.com/features/copilot) (coding agent) to implement changes:

1. A Copilot task is started with a description of the desired change.
2. Copilot creates a new branch and opens a pull request targeting `master`.
3. The PR is reviewed and merged — never pushed directly.

PR titles can be anything descriptive. No special format is required.

### Release Process

Releases are automated. No manual tagging or version bumping needed.

1. Merge PRs to `master` as normal. Every merged PR is automatically included in the next release.
2. After each merge, the `release.yml` workflow creates or updates a **release PR** that bumps the patch version and lists all PRs merged since the last release.
3. When ready to ship, **merge the release PR**. The workflow then creates a git tag, publishes a GitHub release, and uploads the HACS ZIP.

### Branch Protection

The `master` branch has branch protection enabled:
- Pull requests are required before merging.
- Direct pushes to `master` are blocked.

### Local Development

You can still run and test locally:

```bash
# Install dependencies
pip install -r requirements-test.txt

# Run tests
pytest --cov=custom_components.pettracer --cov-report=term -v

# Lint
ruff check custom_components/pettracer/
```

Do your work on a feature branch and open a PR — or use a Copilot task to do it for you.
