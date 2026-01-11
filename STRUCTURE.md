# PetTracer Home Assistant Integration - File Structure

## Overview
Complete custom component for integrating PetTracer GPS pet collars with Home Assistant.

## Directory Structure

```
pettracer-ha/
├── README.md                          # Complete documentation
├── .gitignore                         # Git ignore rules
└── custom_components/
    └── pettracer/
        ├── __init__.py               # Integration setup & data coordinator
        ├── config_flow.py            # UI configuration flow
        ├── const.py                  # Constants and configuration
        ├── device_tracker.py         # Device tracker platform
        ├── manifest.json             # Integration metadata
        ├── strings.json              # UI strings
        └── translations/
            └── en.json               # English translations
```

## File Descriptions

### `manifest.json`
- Defines integration metadata
- Specifies dependency on `pettracer-client>=0.1.0` PyPI package
- Enables config flow UI
- Sets cloud polling as IoT class

### `const.py`
- Domain: `pettracer`
- Update interval: 60 seconds
- Configuration constants

### `__init__.py`
- Async setup and unload functions
- `PetTracerDataUpdateCoordinator` class for data fetching
- Authenticates with PetTracer API
- Manages device list updates
- Handles errors and authentication failures

### `config_flow.py`
- `PetTracerConfigFlow` class for UI setup
- User credential input form
- Credential validation
- Prevents duplicate configurations

### `device_tracker.py`
- `PetTracerDeviceTracker` entity class
- Presents each collar as a GPS device tracker
- Provides GPS coordinates (latitude/longitude)
- Battery level and voltage monitoring
- Additional attributes:
  - Satellite count
  - Signal strength
  - Last contact time
  - Position timestamp
  - Device status and mode
  - Home detection

### `strings.json` & `translations/en.json`
- UI text for configuration flow
- Error messages
- Setup descriptions

## Key Features

1. **Easy Setup**: Config flow UI in Home Assistant
2. **GPS Tracking**: Real-time location for all collars
3. **Battery Monitoring**: Voltage and percentage
4. **Rich Attributes**: Satellites, signal strength, home status
5. **Automatic Updates**: Polls every 60 seconds
6. **Multiple Devices**: Supports all collars in account

## Installation

1. Copy `custom_components/pettracer` to Home Assistant config directory
2. Restart Home Assistant
3. Add integration via UI: Settings → Devices & Services → Add Integration
4. Enter PetTracer credentials

## Requirements

- Home Assistant 2023.1+
- Valid PetTracer account with active subscription
- `pettracer-client` package (auto-installed via requirements)

## API Integration

Uses the official `pettracer-client` library:
- GitHub: https://github.com/AmbientArchitect/petTracer-API
- PyPI: https://pypi.org/project/pettracer-client/

The integration:
1. Authenticates using username/password
2. Fetches all devices in the account
3. Creates device tracker entities
4. Updates location every 60 seconds
5. Handles authentication errors gracefully

## Development Notes

- Built with Home Assistant integration patterns
- Uses `DataUpdateCoordinator` for efficient updates
- Async/await throughout for non-blocking operations
- Config flow prevents duplicate setups via unique_id
- Device info links entities to devices in UI
