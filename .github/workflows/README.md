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

### `hacs.yml` - HACS Validation
Validates the integration is compatible with HACS standards.

Runs on:
- Push to master/main
- Pull requests to master/main
- Manual trigger

### `release.yml` - Release Automation
Automates the release process when a new version is tagged.

Runs on:
- Release publication

Steps:
1. Extracts version from git tag
2. Updates manifest.json with version
3. Creates ZIP archive of the integration
4. Uploads ZIP to GitHub release

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
- Push to master/main/dev branches → Runs tests
- Create pull request → Runs tests and HACS validation
- Publish release → Creates release artifacts

**Manual triggers:**
- Go to Actions tab in GitHub
- Select workflow
- Click "Run workflow"

### Creating a Release

1. Update version in `custom_components/pettracer/manifest.json`
2. Commit and push changes
3. Create and push a tag:
   ```bash
   git tag v0.1.0
   git push origin v0.1.0
   ```
4. Create a release on GitHub
5. Release workflow automatically creates and uploads ZIP

## Status Badges

Add these to your README.md:

```markdown
[![Test](https://github.com/kylegordon/pettracer-ha/workflows/Test/badge.svg)](https://github.com/kylegordon/pettracer-ha/actions/workflows/test.yml)
[![HACS Validation](https://github.com/kylegordon/pettracer-ha/workflows/HACS%20Validation/badge.svg)](https://github.com/kylegordon/pettracer-ha/actions/workflows/hacs.yml)
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
- Ensure tag format is `v*.*.*` (e.g., v0.1.0)
- Check GITHUB_TOKEN has sufficient permissions
- Verify manifest.json is valid JSON
