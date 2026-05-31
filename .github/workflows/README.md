# GitHub Actions Workflows

This directory contains automated workflows for the PetTracer Home Assistant integration.

## Workflows

### `test.yml` - Test Pipeline
Runs on every push and pull request to master, main, or dev branches.

**Jobs:**

1. **Test** - Runs the test suite
   - Tests against Python 3.11 and 3.12
   - Runs pytest with coverage
   - Uploads coverage to Codecov
   - Enforces minimum 80% coverage

2. **Lint** - Code quality checks
   - Runs `ruff` linter
   - Checks code formatting
   - Continues on errors (non-blocking)

3. **Validate** - JSON validation
   - Validates manifest.json
   - Validates strings.json
   - Validates translations
   - Checks HACS compatibility

### `release.yml` - Automated Release Management

Runs on every push to `master`. Every merged PR is automatically included in the next release — no special PR title format required.

**Jobs:**

1. **prepare-release** - Creates or updates a release PR after every merge to master
   - Bumps the patch version in `manifest.json` and `version.txt`
   - Uses GitHub's native release notes generation to list all PRs merged since the last release
   - Skips itself when the release PR is being merged

2. **publish-release** - Runs when the release PR is merged
   - Creates a git tag
   - Publishes a GitHub release with auto-generated notes listing all included PRs
   - Builds and uploads the HACS ZIP (`pettracer-{version}.zip`)

## Usage

### Running Tests Locally
```bash
# Install dependencies
pip install -r requirements-test.txt

# Run tests
pytest --cov=custom_components.pettracer --cov-report=term -v
```

### Triggering Workflows

**Automatic triggers:**
- Push to master/main/dev branches → Runs tests + release workflow
- Create pull request → Runs tests and HACS validation

**Manual triggers:**
- Go to Actions tab in GitHub
- Select workflow
- Click "Run workflow"

### Creating a Release

> **Important:** All changes must go through a pull request. See [CONTRIBUTING.md](../../CONTRIBUTING.md) for the full workflow policy.

Releases are fully automated — **no manual tagging, no special commit format needed**.

1. Merge PRs to `master` as normal.
2. `release.yml` automatically creates or updates a release PR bumping the patch version and listing every merged PR.
3. When ready to release: **merge the release PR**. The workflow creates the tag, publishes the GitHub release, and uploads the HACS ZIP.

## Status Badges

Add these to your README.md:

```markdown
[![Test](https://github.com/kylegordon/pettracer-ha/workflows/Test/badge.svg)](https://github.com/kylegordon/pettracer-ha/actions/workflows/test.yml)
```

## Coverage

Coverage reports are uploaded to Codecov on each test run. To view:
1. Go to https://codecov.io/gh/kylegordon/pettracer-ha
2. Sign in with GitHub
3. View coverage reports and trends

## Troubleshooting

### Tests Failing
- Check the Actions tab for detailed logs
- Run tests locally to reproduce issues
- Ensure all dependencies are in requirements-test.txt

### HACS Validation Failing
- Ensure hacs.json is valid
- Check manifest.json for required fields
- Verify integration follows HACS guidelines

### Release Workflow Issues
- Check GITHUB_TOKEN has `contents: write` and `pull-requests: write` permissions
- Ensure "Allow GitHub Actions to create and approve pull requests" is enabled in repo Settings → Actions → General
- Verify manifest.json is valid JSON
