# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

All development runs inside Docker — do not install dependencies directly on the host.

Build the dev image (required once, and after `requirements-test.txt` changes):
```bash
docker build -f Dockerfile.dev -t pettracer-dev .
```

Run tests with coverage:
```bash
docker run --rm -v "$PWD":/workspace pettracer-dev \
  pytest --cov=custom_components.pettracer --cov-report=term -v
```

Run a single test file:
```bash
docker run --rm -v "$PWD":/workspace pettracer-dev \
  pytest tests/test_sensor.py -v
```

Lint and format:
```bash
docker run --rm -v "$PWD":/workspace pettracer-dev ruff check custom_components/pettracer/
docker run --rm -v "$PWD":/workspace pettracer-dev ruff format custom_components/pettracer/
```

Validate JSON files after editing (CI blocks on invalid JSON):
```bash
docker run --rm -v "$PWD":/workspace pettracer-dev \
  python -m json.tool custom_components/pettracer/manifest.json
```

Open an interactive shell in the container:
```bash
docker run --rm -it -v "$PWD":/workspace pettracer-dev bash
```

## Architecture

This is a Home Assistant custom component that bridges the PetTracer GPS collar cloud API to HA entities. The external `pettracer-client` PyPI package handles all API communication.

**Setup flow:** `config_flow.py` collects credentials → `__init__.py` authenticates and creates a `PetTracerDataUpdateCoordinator` → coordinator is stored in `hass.data[DOMAIN][entry_id]` → three platforms (`binary_sensor`, `device_tracker`, `sensor`) each pull the coordinator from `hass.data` and register entities per device.

**Data flow:** The coordinator calls `client.get_all_devices()` every 60 seconds. Each platform's `async_setup_entry` iterates `coordinator.data["devices"]` and creates entities. Entities extend `CoordinatorEntity` and call `_get_device_data()` to look up their specific device by `device.id` from the coordinator's latest data.

**Sensor pattern:** `sensor.py` uses `PetTracerSensorEntityDescription` (a frozen dataclass extending `SensorEntityDescription`) with a `value_fn: Callable[[device], Any]` field. Adding a new sensor means writing a `_get_*` function and adding an entry to `SENSOR_DESCRIPTIONS` — no new class needed.

**Binary sensors:** `binary_sensor.py` has two concrete classes (`PetTracerAtHomeBinarySensor`, `PetTracerChargingBinarySensor`). These follow the same `CoordinatorEntity` + `_get_device_data()` pattern but are explicit classes rather than description-driven.

## CI Behaviour

- **Tests** (`pytest` job): must pass; enforces ≥80% coverage with `coverage report --fail-under=80`.
- **Validate** job: blocks on invalid JSON in `manifest.json`, `strings.json`, `translations/en.json`, `hacs.json`.
- **Lint** job: `continue-on-error: true` — linting failures do not block CI.
- Changing the `version` field in `manifest.json` triggers the auto-release workflow (creates a GitHub release and HACS ZIP). Don't bump the version unless you intend a release.
