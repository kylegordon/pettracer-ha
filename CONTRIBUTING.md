# Contributing to PetTracer Home Assistant Integration

## Workflow Policy: PRs Only — No Direct Commits to `master`

**All changes must be made via a pull request. Direct commits to `master` are not allowed.**

This applies to everyone — including automated tools and maintainers.

### How Changes Are Made

This repository uses [GitHub Copilot](https://github.com/features/copilot) (coding agent) to implement changes:

1. A Copilot task is started with a description of the desired change.
2. Copilot creates a new branch (e.g. `copilot/my-feature`) and implements the change there.
3. Copilot opens a pull request targeting `master`.
4. The PR is reviewed and merged via GitHub — never pushed directly.

### Release Process

Releases are fully automated via [release-please](https://github.com/googleapis/release-please). **No manual tagging or version bumping is required.**

#### How it works

1. Merge PRs to `master` using [conventional commit](https://www.conventionalcommits.org/) prefixes:
   - `feat: …` → bumps minor version (e.g. 1.0.5 → 1.1.0)
   - `fix: …` → bumps patch version (e.g. 1.0.5 → 1.0.6)
   - `chore: …`, `docs: …`, etc. → no version bump (included in changelog)
   - `feat!: …` or `fix!: …` (breaking change) → bumps major version

2. After each merge, the `release-please.yml` workflow automatically creates or updates a **release PR** that:
   - Bumps `version.txt` and `custom_components/pettracer/manifest.json`
   - Updates `CHANGELOG.md`

3. When you're ready to release, **merge the release PR**. Release-please then:
   - Creates a git tag (e.g. `v1.0.6`)
   - Publishes a GitHub release with changelog notes
   - Triggers the HACS ZIP artifact upload

There is no step 4 — no manual tagging, no manual version edits.

> **Important:** Only `fix:` and `feat:` commits (and breaking-change variants) trigger a release PR.
> `chore:`, `docs:`, `refactor:`, `test:`, and `ci:` commits are tracked in the changelog but do **not**
> create a release PR on their own. If only non-releasable commits have been merged since the last
> release, the release-please workflow will run successfully but produce no PR — this is expected.

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
