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

Releases are triggered by pushing a version tag **after** the version bump has been merged via PR:

1. Open a Copilot task to bump the version in `custom_components/pettracer/manifest.json`.
2. Let Copilot create a branch and PR for the version bump.
3. Review and merge the PR.
4. Tag the merge commit and push the tag:
   ```bash
   git fetch origin
   git tag vX.Y.Z origin/master
   git push origin vX.Y.Z
   ```
5. The `release-on-tag.yml` workflow automatically creates the GitHub release.

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
