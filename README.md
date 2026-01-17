# PetTracer Home Assistant Integration

[![Test](https://github.com/kylegordon/pettracer-ha/workflows/Test/badge.svg)](https://github.com/kylegordon/pettracer-ha/actions/workflows/test.yml)

> **⚠️ DISCLAIMER**: This project is not affiliated with, endorsed by, or in any way officially connected with PetTracer.com or its parent company. This is an independent, unofficial integration created by the community. PetTracer® is a trademark of its respective owner.

A custom Home Assistant integration for [PetTracer](https://www.pettracer.com/) GPS pet collars. Track your pets' locations directly in Home Assistant!

This integration uses the [petTracer-API](https://github.com/AmbientArchitect/petTracer-API) client library to connect to the PetTracer service.

## Features

- 📍 **Device Tracking**: Each collar appears as a trackable device in Home Assistant
- 🗺️ **GPS Coordinates**: Real-time latitude/longitude coordinates for all your pet collars
- 🔋 **Battery Monitoring**: See battery level and voltage for each collar
- 📡 **Signal Quality**: View satellite count and signal strength information
- 🏠 **Home Detection**: Track whether your pet is at home
- 📊 **Individual Sensors**: Each attribute is exposed as a separate sensor entity with appropriate device classes
- 🔄 **Automatic Updates**: Location updates every 60 seconds

## Requirements

- Home Assistant 2023.1 or newer
- A PetTracer GPS collar with active subscription
- Valid PetTracer account credentials

## Installation

### HACS (Recommended)

This integration can be installed via HACS as a **custom repository**.

1. **Add and install this repository in HACS:**
   - Open HACS in Home Assistant
   - Click on "Integrations"
   - Click the three dots (⋮) in the top right corner
   - Select "Custom repositories"
   - In the "Repository" field, enter: `https://github.com/kylegordon/pettracer-ha`
   - In the "Category" dropdown, select "Integration"
   - Click "Add"
   - Find "PetTracer GPS Tracker" in your integrations list
   - Click on the integration
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

### Sensors

Each collar provides the following individual sensor entities:

#### Battery Sensors
- **Battery Level** (`sensor.pet_name_battery_level`)
  - Device class: Battery
  - Unit: %
  - Calculated from battery voltage (3.0V-4.2V range)
  
- **Battery Voltage** (`sensor.pet_name_battery_voltage`)
  - Device class: Voltage
  - Unit: mV
  - Raw battery voltage reading

#### Location Sensors
- **Latitude** (`sensor.pet_name_latitude`)
  - GPS latitude coordinate
  
- **Longitude** (`sensor.pet_name_longitude`)
  - GPS longitude coordinate
  
- **GPS Accuracy** (`sensor.pet_name_gps_accuracy`)
  - Device class: Distance
  - Unit: m
  - GPS position accuracy in meters

#### Communication Sensors
- **Last Contact** (`sensor.pet_name_last_contact`)
  - Device class: Timestamp
  - Last time the collar contacted the server
  
- **Position Time** (`sensor.pet_name_position_time`)
  - Device class: Timestamp
  - Timestamp when GPS position was measured

#### Signal Sensors
- **Satellites** (`sensor.pet_name_satellites`)
  - Number of GPS satellites in use
  
- **Signal Strength** (`sensor.pet_name_signal_strength`)
  - Device class: Signal strength
  - Unit: dBm
  - Cellular signal strength (RSSI)

#### Status Sensors
- **Status** (`sensor.pet_name_status`)
  - Device status code
  
- **Mode** (`sensor.pet_name_mode`)
  - Device operating mode
  
- **At Home** (`sensor.pet_name_at_home`)
  - Text sensor indicating if pet is at home ("true" or "false")

### Example Automations

**Alert when pet leaves home:**
```yaml
automation:
  - alias: "Pet Left Home"
    trigger:
      - platform: state
        entity_id: sensor.your_pet_name_at_home
        to: "false"
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
        entity_id: sensor.your_pet_name_battery_level
        below: 20
    action:
      - service: notify.mobile_app
        data:
          title: "Battery Warning"
          message: "Pet collar battery is low ({{ states('sensor.your_pet_name_battery_level') }}%)"
```

**Notify when GPS accuracy is poor:**
```yaml
automation:
  - alias: "Pet Collar Poor GPS"
    trigger:
      - platform: numeric_state
        entity_id: sensor.your_pet_name_gps_accuracy
        above: 50
    action:
      - service: notify.mobile_app
        data:
          title: "GPS Warning"
          message: "Pet collar has poor GPS accuracy ({{ states('sensor.your_pet_name_gps_accuracy') }}m)"
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
