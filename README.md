# PetTracer Home Assistant Integration

[![Test](https://github.com/kylegordon/pettracer-ha/workflows/Test/badge.svg)](https://github.com/kylegordon/pettracer-ha/actions/workflows/test.yml)
[![HACS Validation](https://github.com/kylegordon/pettracer-ha/workflows/HACS%20Validation/badge.svg)](https://github.com/kylegordon/pettracer-ha/actions/workflows/hacs.yml)

A custom Home Assistant integration for [PetTracer](https://www.pettracer.com/) GPS pet collars. Track your pets' locations directly in Home Assistant!

This integration uses the [petTracer-API](https://github.com/AmbientArchitect/petTracer-API) client library to connect to the PetTracer service.

## Features

- 📍 **Device Tracking**: Each collar appears as a trackable device in Home Assistant
- 🗺️ **GPS Coordinates**: Real-time latitude/longitude coordinates for all your pet collars
- 🔋 **Battery Monitoring**: See battery level and voltage for each collar
- 📡 **Signal Quality**: View satellite count and signal strength information
- 🏠 **Home Detection**: Track whether your pet is at home
- 🔄 **Automatic Updates**: Location updates every 60 seconds

## Requirements

- Home Assistant 2023.1 or newer
- A PetTracer GPS collar with active subscription
- Valid PetTracer account credentials

## Installation

### HACS (Recommended)

1. Add this repository as a custom repository in HACS:
   - Open HACS in Home Assistant
   - Click on "Integrations"
   - Click the three dots in the top right corner
   - Select "Custom repositories"
   - Add the repository URL and select "Integration" as the category
   - Click "Add"

2. Install the integration:
   - Find "PetTracer GPS Tracker" in HACS
   - Click "Download"
   - Restart Home Assistant

### Manual Installation

1. Copy the `custom_components/pettracer` directory to your Home Assistant configuration directory:
   ```bash
   cd /path/to/homeassistant/config
   mkdir -p custom_components
   cp -r /path/to/pettracer-ha/custom_components/pettracer custom_components/
   ```
   
   The final path should be: `custom_components/pettracer/`

2. Restart Home Assistant

## Configuration

### Using the UI (Recommended)

1. Go to **Settings** → **Devices & Services**
2. Click **+ Add Integration**
3. Search for "PetTracer"
4. Enter your PetTracer username and password
5. Click **Submit**

Your pet collars will appear as device trackers in Home Assistant.

### Using configuration.yaml (Legacy)

This integration supports config flow only. Configuration via `configuration.yaml` is not supported.

## Usage

### Device Trackers

Each collar appears as a device tracker entity with the pet's name:
- Entity ID format: `device_tracker.pet_name`
- Shows current GPS location on the map
- Updates automatically every 60 seconds

### Attributes

Each device tracker provides additional attributes:

- `battery_voltage_mv`: Battery voltage in millivolts
- `last_contact`: Last time the collar contacted the server
- `satellites`: Number of GPS satellites in use
- `signal_strength`: Signal strength (RSSI)
- `position_time`: Timestamp of the GPS position
- `status`: Device status code
- `mode`: Device operating mode
- `at_home`: Boolean indicating if pet is at home

### Example Automations

**Alert when pet leaves home:**
```yaml
automation:
  - alias: "Pet Left Home"
    trigger:
      - platform: state
        entity_id: device_tracker.your_pet_name
        attribute: at_home
        to: false
    action:
      - service: notify.mobile_app
        data:
          title: "Pet Alert"
          message: "Your pet has left home!"
```

**Low battery warning:**
```yaml
automation:
  - alias: "Pet Collar Low Battery"
    trigger:
      - platform: numeric_state
        entity_id: device_tracker.your_pet_name
        attribute: battery_level
        below: 20
    action:
      - service: notify.mobile_app
        data:
          title: "Battery Warning"
          message: "Pet collar battery is low ({{ state_attr('device_tracker.your_pet_name', 'battery_level') }}%)"
```

## Troubleshooting

### Authentication Errors

If you receive authentication errors:
- Verify your username and password are correct
- Check that your PetTracer subscription is active
- Try logging into the PetTracer website/app to confirm credentials

### No Location Data

If location data isn't showing:
- Ensure the collar has GPS signal (check satellite count)
- Verify the collar is powered on and charged
- Check the collar's last contact time - it may be out of range

### Integration Not Loading

If the integration fails to load:
- Check Home Assistant logs for errors
- Ensure the `pettracer-client` library is installed (should be automatic)
- Restart Home Assistant after installation

## Development

This integration is built using:
- [petTracer-API Python client](https://github.com/AmbientArchitect/petTracer-API)
- Home Assistant integration framework
- Config flow for easy setup

### File Structure

```
custom_components/pettracer/
├── __init__.py          # Integration setup and coordinator
├── config_flow.py       # UI configuration flow
├── const.py            # Constants
├── device_tracker.py   # Device tracker platform
├── manifest.json       # Integration metadata
├── strings.json        # UI strings
└── translations/
    └── en.json         # English translations
```

## Support

For issues related to:
- **This Home Assistant integration**: Open an issue in this repository
- **The PetTracer API client**: Visit [petTracer-API repository](https://github.com/AmbientArchitect/petTracer-API)
- **PetTracer service**: Contact [PetTracer support](https://www.pettracer.com/)

## License

MIT License

## Disclaimer

This is an unofficial integration. PetTracer® is a trademark of its respective owner. Use this integration at your own risk and respect the PetTracer service terms of use.
