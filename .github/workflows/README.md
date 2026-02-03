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

### `release-on-tag.yml` - Tag-Based Release Automation
Automatically creates releases when a new version tag is pushed.

Runs on:
- Push of tags matching `v*.*.*` pattern (e.g., v1.0.0, v1.2.3)

Steps:
1. Extracts version from tag name
2. Generates automated release notes including:
   - PR titles and authors from commits between tags
   - Full commit history
   - Installation instructions
3. Creates ZIP archive of the integration
4. Creates GitHub release with generated notes and ZIP artifact

### `auto-release.yml` - Legacy Manifest-Based Release
Legacy workflow that creates releases when manifest.json version changes.

**Note:** With the new tag-based workflow, this can be disabled or removed. Use `release-on-tag.yml` for new releases.

### `release.yml` - Manual Release Support
Supports manually published releases.

**Note:** With the new tag-based workflow, this is mainly for backward compatibility.

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
- Push tag matching v*.*.* → Creates release with automated notes

**Manual triggers:**
- Go to Actions tab in GitHub
- Select workflow
- Click "Run workflow"

### Creating a Release

**New Tag-Based Process (Recommended):**

1. Update version in `custom_components/pettracer/manifest.json`
2. Commit and push changes to master:
   ```bash
   git add custom_components/pettracer/manifest.json
   git commit -m "Bump version to 1.0.4"
   git push origin master
   ```
3. Create and push a version tag:
   ```bash
   git tag v1.0.4
   git push origin v1.0.4
   ```
4. The `release-on-tag.yml` workflow automatically:
   - Generates release notes from PRs and commits
   - Creates a ZIP package
   - Publishes the GitHub release

**Legacy Process (auto-release.yml):**
- Pushing changes to manifest.json triggers auto-release
- Can be disabled in favor of tag-based releases

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
