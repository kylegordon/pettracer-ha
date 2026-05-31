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

### `release-please.yml` - Automated Release Management

Runs on every push to `master`. Uses [release-please](https://github.com/googleapis/release-please) to automate versioning and releases.

**Jobs:**

1. **release-please** - Creates or updates a release PR when new commits land on master
   - Reads conventional commit prefixes (`feat:`, `fix:`, `chore:`, etc.) to determine the next version
   - Keeps `version.txt` and `custom_components/pettracer/manifest.json` in sync
   - Updates `CHANGELOG.md`

2. **upload-artifact** - Runs only when a release PR is merged
   - Builds the HACS-compatible ZIP (`pettracer-{version}.zip`)
   - Uploads the ZIP to the GitHub release

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
- Push to master/main/dev branches → Runs tests + release-please
- Create pull request → Runs tests and HACS validation

**Manual triggers:**
- Go to Actions tab in GitHub
- Select workflow
- Click "Run workflow"

### Creating a Release

> **Important:** All changes must go through a pull request. See [CONTRIBUTING.md](../../CONTRIBUTING.md) for the full workflow policy.

Releases are fully automated — **no manual tagging or version bumping needed**.

1. Merge PRs to `master` using conventional commit prefixes:
   - `feat: …` → minor bump, `fix: …` → patch bump, `feat!: …` → major bump
2. `release-please.yml` automatically creates or updates a release PR with updated changelog and version files.
3. When ready to release: **merge the release PR**. Release-please creates the tag, publishes the GitHub release, and triggers the ZIP artifact upload.

See [CONTRIBUTING.md](../../CONTRIBUTING.md) for the full conventional commits reference.

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
- Verify `release-please-config.json` and `.release-please-manifest.json` are valid JSON
- Verify manifest.json is valid JSON (updated automatically by release-please)
