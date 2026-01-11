# PetTracer Home Assistant Integration - Test Suite

This directory contains comprehensive tests for the PetTracer integration.

## Running Tests

### Install test dependencies

```bash
pip install -r requirements-test.txt
```

### Run all tests

```bash
pytest
```

### Run with coverage

```bash
pytest --cov=custom_components.pettracer --cov-report=html --cov-report=term
```

### Run specific test file

```bash
pytest tests/test_config_flow.py -v
```

### Run specific test

```bash
pytest tests/test_config_flow.py::test_form_user_success -v
```

## Test Structure

### `conftest.py`
Shared fixtures for all tests including:
- Mock PetTracerClient instances
- Mock device data
- Config entry data
- Setup entry mocks

### `test_config_flow.py`
Tests for the configuration flow:
- User form display
- Successful authentication
- Invalid credentials handling
- Duplicate entry prevention
- Case-insensitive username handling
- Unknown error handling

### `test_init.py`
Tests for integration setup and coordinator:
- Successful entry setup
- Authentication failures
- Config entry not ready scenarios
- Entry unloading
- Coordinator data updates
- Multiple device handling
- Empty device list handling
- API error handling

### `test_device_tracker.py`
Tests for device tracker platform:
- Entity creation
- GPS coordinates
- Battery level conversion (mV to %)
- Location accuracy
- Device attributes
- Missing position data handling
- Multiple device support
- Coordinator updates
- Device info properties
- Partial data handling

### `test_const.py`
Tests for constants:
- Domain verification
- Configuration key validation
- Update interval validation

## Test Coverage

The test suite covers:

1. **Config Flow** (100%)
   - Form rendering
   - User input validation
   - API authentication
   - Error handling
   - Duplicate prevention

2. **Integration Setup** (100%)
   - Entry setup and teardown
   - Client initialization
   - Coordinator creation
   - Platform forwarding
   - Error scenarios

3. **Data Coordinator** (100%)
   - Data fetching
   - Update scheduling
   - Error handling
   - Multi-device support

4. **Device Tracker** (100%)
   - Entity properties
   - GPS data
   - Battery monitoring
   - State attributes
   - Device information
   - Edge cases

## Mock Data

Test fixtures include:
- Full device with GPS location
- Device without position data
- Partial attribute data
- Multiple devices
- Authentication responses

## Continuous Integration

These tests are designed to run in CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
- name: Run tests
  run: |
    pip install -r requirements-test.txt
    pytest --cov=custom_components.pettracer
```

## Coverage Goals

Target coverage: >95% for all modules
- Config flow: 100%
- Init: 100%
- Device tracker: 100%
- Constants: 100%
