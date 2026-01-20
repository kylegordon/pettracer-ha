# PetTracer Home Assistant Integration - Copilot Instructions

## Repository Overview

This is a **Home Assistant custom integration** for PetTracer GPS pet collars. It's a small Python project (~734 lines of code) that provides device tracking and sensor entities for pet location monitoring.

**Key Facts:**
- **Type:** Home Assistant custom component (HACS-compatible)
- **Language:** Python 3.12+
- **Framework:** Home Assistant 2023.1+
- **Dependencies:** pettracer-client>=0.1.0 (from PyPI)
- **Size:** 5 Python source files, 7 test files, 47 unit tests
- **Test Coverage:** 96% (minimum required: 80%)
- **Lines of Code:** ~734 lines in source, comprehensive test suite

## Project Structure

```
pettracer-ha/
├── custom_components/pettracer/    # Main integration code
│   ├── __init__.py                 # Integration setup & DataUpdateCoordinator
│   ├── config_flow.py              # UI configuration flow
│   ├── const.py                    # Constants (DOMAIN, UPDATE_INTERVAL_SECONDS)
│   ├── device_tracker.py           # Device tracker entities (~104 lines)
│   ├── sensor.py                   # Sensor entities (~216 lines)
│   ├── manifest.json               # Integration metadata (CRITICAL)
│   ├── strings.json                # UI strings
│   └── translations/en.json        # English translations
├── tests/                          # Test suite (pytest)
│   ├── conftest.py                 # Test fixtures
│   ├── test_config_flow.py
│   ├── test_const.py
│   ├── test_device_tracker.py
│   ├── test_init.py
│   └── test_sensor.py
├── .github/workflows/              # CI/CD automation
│   ├── test.yml                    # Main test pipeline (runs on PR/push)
│   ├── release.yml                 # Release automation
│   └── auto-release.yml            # Auto-release on manifest.json version change
├── pyproject.toml                  # Pytest & coverage configuration
├── requirements-test.txt           # Test dependencies
├── hacs.json                       # HACS compatibility metadata
└── README.md, STRUCTURE.md         # Documentation
```

## Critical Build & Test Commands

### Installation & Setup

**ALWAYS run these commands in sequence before testing:**

```bash
# 1. Install test dependencies (REQUIRED - takes ~60 seconds)
pip install -r requirements-test.txt

# 2. Install runtime dependencies (REQUIRED)
pip install pettracer-client homeassistant
```

**Important:** The `pytest-homeassistant-custom-component` package automatically installs Home Assistant. Do NOT install homeassistant separately unless already done.

### Testing

**Run tests with coverage (PRIMARY validation method):**

```bash
pytest --cov=custom_components.pettracer --cov-report=term -v
```

**Expected result:**
- All 47 tests pass
- Coverage ≥80% (currently 96%)
- Test runtime: ~2 seconds

**Run specific test file:**

```bash
pytest tests/test_config_flow.py -v
```

**Common test issues:**
- If tests fail with import errors, ensure both test and runtime dependencies are installed
- Async tests use `pytest-asyncio` with `asyncio_mode = "auto"` (configured in pyproject.toml)

### Linting

**Check code with ruff (runs in CI):**

```bash
# Install ruff first
pip install ruff

# Check for lint errors
ruff check custom_components/pettracer/ --output-format=github

# Check formatting (NOTE: continue-on-error in CI)
ruff format --check custom_components/pettracer/
```

**Important:** Formatting checks are non-blocking in CI (`continue-on-error: true`). Lint errors are also non-blocking but should be fixed if possible.

### JSON Validation

**ALWAYS validate JSON files after editing:**

```bash
# Validate all JSON files (runs in CI validate job)
python -c "import json; json.load(open('custom_components/pettracer/manifest.json'))"
python -c "import json; json.load(open('custom_components/pettracer/strings.json'))"
python -c "import json; json.load(open('custom_components/pettracer/translations/en.json'))"
python -c "import json; json.load(open('hacs.json'))"
```

**Critical:** Invalid JSON in manifest.json will break the integration completely.

## CI/CD Pipeline

The repository uses GitHub Actions with **3 workflows** that run on every push/PR:

### test.yml (Main Validation Pipeline)

**Triggers:** Push/PR to master, main, or dev branches

**3 Jobs:**

1. **test** - Run test suite
   - Python 3.x (uses latest 3.12)
   - Installs: requirements-test.txt + pettracer-client + homeassistant
   - Runs: `pytest --cov=custom_components.pettracer --cov-report=xml --cov-report=term -v`
   - Uploads coverage to Codecov
   - **Enforces minimum 80% coverage** with `coverage report --fail-under=80`
   - **This job MUST pass**

2. **lint** - Code quality (NON-BLOCKING)
   - Python 3.12
   - Runs: `ruff check` and `ruff format --check`
   - Both steps have `continue-on-error: true` (won't fail CI)
   - Fix linting issues when possible, but not required

3. **validate** - JSON validation (BLOCKING)
   - Validates manifest.json, strings.json, translations, hacs.json
   - **This job MUST pass**

### auto-release.yml (Version-based Release)

**Triggers:** Push to master when `custom_components/pettracer/manifest.json` changes

**Behavior:**
- Automatically creates GitHub release when manifest.json version is updated
- Creates ZIP package for HACS installation
- **Important:** Only updates manifest.json version when making a release

### release.yml (Manual Release)

**Triggers:** Manual release publication

**Behavior:** Creates release artifacts when release is manually published

## Making Code Changes

### Typical Development Workflow

1. **Make changes** to files in `custom_components/pettracer/`
2. **Run tests immediately:**
   ```bash
   pytest --cov=custom_components.pettracer --cov-report=term -v
   ```
3. **Fix any test failures** before proceeding
4. **Validate JSON** if you edited manifest.json, strings.json, or translations
5. **Run linting** (optional but recommended):
   ```bash
   ruff check custom_components/pettracer/
   ruff format --check custom_components/pettracer/
   ```
6. **Update tests** if you changed functionality
7. **Verify coverage** stays ≥80%

### Common File Edit Patterns

**Editing manifest.json:**
- ALWAYS validate JSON syntax after editing
- Version format: "X.Y.Z" (e.g., "1.0.1")
- Changing version triggers auto-release workflow
- Required fields: domain, name, version, requirements, documentation, codeowners

**Editing Python files:**
- Follow existing code patterns
- Use async/await for I/O operations
- Use Home Assistant's DataUpdateCoordinator pattern (see __init__.py)
- Add corresponding tests in tests/ directory
- Import from homeassistant.const for standard constants

**Adding new sensor types:**
- Edit sensor.py to add new sensor class
- Add test in test_sensor.py
- Update device_tracker.py if needed for device tracker attributes

### Test Development

**Test fixtures** are in `tests/conftest.py`:
- `mock_pettracer_client` - Mock API client
- `mock_device` - Mock device with full data
- `mock_device_no_position` - Mock device without GPS data
- All tests use pytest-homeassistant-custom-component fixtures

**Test patterns:**
- Use `@pytest.mark.asyncio` for async tests (auto-enabled via pyproject.toml)
- Mock the PetTracerClient from pettracer library
- Use HomeAssistant test fixtures from pytest-homeassistant-custom-component
- Coverage requirement: 80% minimum, currently at 96%

## Key Architecture Details

### Integration Flow
1. **Config Flow** (config_flow.py): User enters credentials via UI
2. **Setup** (__init__.py): Authenticates with PetTracerClient, creates DataUpdateCoordinator
3. **Platforms**: Forwards to device_tracker and sensor platforms
4. **Updates**: Coordinator polls every 60 seconds (UPDATE_INTERVAL_SECONDS)

### Data Flow
- PetTracerClient (external library) → DataUpdateCoordinator → Entities
- Coordinator calls `client.get_all_devices()` every 60 seconds
- Each device creates: 1 device_tracker + 12 sensor entities

### Entity Structure
**Device Tracker** (device_tracker.py):
- Shows pet location on map
- Provides GPS coordinates, battery, and metadata as attributes

**Sensors** (sensor.py):
- Battery Level (%), Battery Voltage (mV)
- Latitude, Longitude, GPS Accuracy (m)
- Last Contact (timestamp), Position Time (timestamp)
- Satellites (count), Signal Strength (dBm)
- Status, Mode, At Home (text)

### Important Constants (const.py)
- `DOMAIN = "pettracer"`
- `UPDATE_INTERVAL_SECONDS = 60`
- `CONF_USERNAME`, `CONF_PASSWORD` for credentials

## Troubleshooting Common Issues

### Tests fail with "ModuleNotFoundError: pettracer"
**Solution:** Run `pip install pettracer-client`

### Tests fail with Home Assistant import errors
**Solution:** Run `pip install -r requirements-test.txt` (includes pytest-homeassistant-custom-component which installs Home Assistant)

### Coverage drops below 80%
**Solution:** Add tests for new code or remove untested code paths

### JSON validation fails
**Solution:** Check JSON syntax with an online validator or `python -m json.tool filename.json`

### CI "validate" job fails
**Solution:** Run local JSON validation commands listed above

### Formatting check fails in CI
**Solution:** Non-blocking in CI, but run `ruff format custom_components/pettracer/` to auto-fix

## Best Practices for This Repository

1. **ALWAYS run tests before committing** - Takes only 2 seconds
2. **Never break JSON files** - Validate after every edit to manifest.json
3. **Maintain ≥80% coverage** - CI will fail below this threshold
4. **Don't change version in manifest.json** unless making a release (triggers auto-release)
5. **Follow Home Assistant patterns** - Use DataUpdateCoordinator, proper device classes
6. **Mock external dependencies** - Never call real PetTracer API in tests
7. **Keep changes minimal** - This is a small, focused integration
8. **Update tests with code** - Don't break existing tests

## Documentation Files

- **README.md** - User-facing documentation, installation, usage examples
- **STRUCTURE.md** - Detailed file structure and architecture
- **.github/workflows/README.md** - CI/CD documentation
- **tests/README.md** - Test suite documentation and coverage goals

## Quick Reference

**Test command:** `pytest --cov=custom_components.pettracer --cov-report=term -v`
**Lint command:** `ruff check custom_components/pettracer/`
**Format command:** `ruff format custom_components/pettracer/`
**Validate JSON:** `python -c "import json; json.load(open('custom_components/pettracer/manifest.json'))"`

**Dependencies to install:** `pip install -r requirements-test.txt && pip install pettracer-client homeassistant`

**CI passes when:**
- All 47 tests pass
- Coverage ≥80%
- All JSON files are valid
- (Linting failures are non-blocking)

## Final Notes

This repository follows Home Assistant custom component standards and is HACS-compatible. Changes should maintain compatibility with Home Assistant 2023.1+ and follow the existing patterns for coordinators, entities, and config flows. The test suite is comprehensive (96% coverage) and should be maintained at that level.

**Trust these instructions.** Only search for additional information if something is unclear, incorrect, or if you're adding new functionality not covered here.
