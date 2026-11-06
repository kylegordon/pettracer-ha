# Contributing to PetTracer Home Assistant Integration

## Workflow Policy: PRs Only — No Direct Commits to `master`

**All changes must be made via a pull request. Direct commits to `master` are not allowed.**

This applies to everyone — including automated tools and maintainers.

### How Changes Are Made

This repository uses [GitHub Copilot](https://github.com/features/copilot) (coding agent) to implement changes:

1. A Copilot task is started with a description of the desired change.
2. Copilot creates a new branch and opens a pull request targeting `master`.
3. The PR is reviewed and merged — never pushed directly.

### Merge Strategy and PR Titles

This repository uses **squash merges only**. When a PR is merged, GitHub creates a single commit on `master` using the PR title as the commit message.

PR titles can be anything descriptive. No special format is required.

Label each PR so the release notes group it: `enhancement` (Features), `bug` (Fixes), or `chore` (Chores). Dependabot and Renovate PRs get `dependencies` automatically and land under Chores. Unlabelled PRs appear under Other changes. Categories are set in `.github/release.yml`.

### Release Process

Releases are automated. No manual tagging or version bumping needed.

1. Merge PRs to `master` as normal. Every merged PR is automatically included in the next release.
2. After each merge, the `.github/workflows/release.yml` workflow creates or updates a **release PR** that bumps the patch version and lists all PRs merged since the last release.
3. When ready to ship, **merge the release PR**. The workflow then creates a git tag, publishes a GitHub release, and uploads the HACS ZIP.

### Branch Protection

The `master` branch has branch protection enabled:
- Pull requests are required before merging.
- Direct pushes to `master` are blocked.

### Local Development

Development runs in Docker; don't install dependencies on the host:

```bash
# Build the dev image (again after requirements-test.txt or manifest.json changes)
docker build -f Dockerfile.dev -t pettracer-dev .

# Run tests
docker run --rm -v "$PWD":/workspace pettracer-dev \
  pytest --cov=custom_components.pettracer --cov-branch --cov-report=term -v

# Lint and format check (both block CI)
docker run --rm -v "$PWD":/workspace pettracer-dev ruff check custom_components/pettracer/
docker run --rm -v "$PWD":/workspace pettracer-dev ruff format --check custom_components/pettracer/
```

Do your work on a feature branch and open a PR — or use a Copilot task to do it for you.
