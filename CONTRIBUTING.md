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

### Merge Strategy and PR Titles

This repository uses **squash merges only**. When a PR is merged, GitHub creates a single commit on `master` using the PR title as the commit message.

**PR titles must follow [conventional commit](https://www.conventionalcommits.org/) format** — this is how release-please determines what changed and whether a release is needed:

| PR title prefix | Effect |
|---|---|
| `fix: …` | Patch version bump; included in release notes |
| `feat: …` | Minor version bump; included in release notes |
| `fix!: …` / `feat!: …` | Major version bump (breaking change) |
| `chore: …`, `docs: …`, `refactor: …`, `test: …`, `ci: …` | No version bump; included in changelog but do **not** trigger a release PR |

> **Why this matters:** Release-please reads the squash commit message (i.e. the PR title) to decide what to include in the release PR. A PR merged without a conventional commit title will be invisible to release-please.

### Release Process

Releases are fully automated via [release-please](https://github.com/googleapis/release-please). **No manual tagging or version bumping is required.**

#### How it works

1. Merge PRs to `master` with conventional commit PR titles (see table above).
   Release-please reads the squash commit message (= PR title) to build the release.

2. After each merge, the `release-please.yml` workflow automatically creates or updates a **release PR** that:
   - Bumps `version.txt` and `custom_components/pettracer/manifest.json`
   - Updates `CHANGELOG.md`

3. When you're ready to release, **merge the release PR**. Release-please then:
   - Creates a git tag (e.g. `v1.0.6`)
   - Publishes a GitHub release with changelog notes
   - Triggers the HACS ZIP artifact upload

There is no step 4 — no manual tagging, no manual version edits.

> **Note:** If only `chore:`, `docs:`, `refactor:`, `test:`, or `ci:` PRs have been merged since the last
> release, the workflow will run successfully but produce no release PR — this is expected behaviour.

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
