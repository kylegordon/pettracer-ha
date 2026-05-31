"""Tests for the PetTracer sensor platform."""

from unittest.mock import MagicMock, patch

from pytest_homeassistant_custom_component.common import MockConfigEntry

from homeassistant.const import CONF_PASSWORD, CONF_USERNAME, EntityCategory
from homeassistant.config_entries import ConfigEntryState
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorStateClass,
)

from custom_components.pettracer.const import DOMAIN
from custom_components.pettracer.sensor import (
    SENSOR_DESCRIPTIONS,
    PetTracerSensor,
)


async def test_sensor_setup(hass, mock_pettracer_client_init, mock_device):
    """Test sensor entities are created."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={
            CONF_USERNAME: "test@example.com",
            CONF_PASSWORD: "test_password",
        },
        entry_id="test_entry",
    )
    entry.add_to_hass(hass)

    # Set the entry state to SETUP_IN_PROGRESS to allow async_config_entry_first_refresh
    entry._async_set_state(hass, ConfigEntryState.SETUP_IN_PROGRESS, None)

    mock_pettracer_client_init.get_all_devices.return_value = [mock_device]

    with patch("custom_components.pettracer.PetTracerClient") as mock_client:
        mock_client.return_value = mock_pettracer_client_init

        from custom_components.pettracer import async_setup_entry
        from custom_components.pettracer.sensor import async_setup_entry as sensor_setup

        # Setup integration
        with patch(
            "homeassistant.config_entries.ConfigEntries.async_forward_entry_setups"
        ):
            await async_setup_entry(hass, entry)

        # Setup sensor platform
        entities = []

        def mock_add_entities(new_entities, update_before_add):
            entities.extend(new_entities)

        await sensor_setup(hass, entry, mock_add_entities)

        # Should create 11 sensors per device (AtHome moved to binary_sensor)
        assert len(entities) == 11


async def test_battery_sensor(hass, mock_device):
    """Test battery level sensor."""
    coordinator = MagicMock()
    coordinator.data = {"devices": [mock_device]}

    description = next(d for d in SENSOR_DESCRIPTIONS if d.key == "battery_level")
    sensor = PetTracerSensor(coordinator, mock_device, description)

    assert sensor.unique_id == "pettracer_12345_battery_level"
    assert sensor.name == "Fluffy Battery Level"
    assert sensor.device_class == SensorDeviceClass.BATTERY
    assert sensor.native_unit_of_measurement == "%"
    assert sensor.state_class == SensorStateClass.MEASUREMENT

    # Test battery conversion (4100mV should be 83%)
    battery = sensor.native_value
    assert battery == 83



async def test_battery_voltage_sensor(hass, mock_device):
    """Test battery voltage sensor."""
    coordinator = MagicMock()
    coordinator.data = {"devices": [mock_device]}

    description = next(d for d in SENSOR_DESCRIPTIONS if d.key == "battery_voltage")
    sensor = PetTracerSensor(coordinator, mock_device, description)

    assert sensor.unique_id == "pettracer_12345_battery_voltage"
    assert sensor.name == "Fluffy Battery Voltage"
    assert sensor.device_class == SensorDeviceClass.VOLTAGE
    assert sensor.native_unit_of_measurement == "mV"
    assert sensor.state_class == SensorStateClass.MEASUREMENT
    assert sensor.entity_category == EntityCategory.DIAGNOSTIC
    assert sensor.native_value == 4100


async def test_latitude_sensor(hass, mock_device):
    """Test latitude sensor."""
    coordinator = MagicMock()
    coordinator.data = {"devices": [mock_device]}

    description = next(d for d in SENSOR_DESCRIPTIONS if d.key == "latitude")
    sensor = PetTracerSensor(coordinator, mock_device, description)

    assert sensor.unique_id == "pettracer_12345_latitude"
    assert sensor.name == "Fluffy Latitude"
    assert sensor.state_class == SensorStateClass.MEASUREMENT
    assert sensor.native_value == 51.5074


async def test_longitude_sensor(hass, mock_device):
    """Test longitude sensor."""
    coordinator = MagicMock()
    coordinator.data = {"devices": [mock_device]}

    description = next(d for d in SENSOR_DESCRIPTIONS if d.key == "longitude")
    sensor = PetTracerSensor(coordinator, mock_device, description)

    assert sensor.unique_id == "pettracer_12345_longitude"
    assert sensor.name == "Fluffy Longitude"
    assert sensor.state_class == SensorStateClass.MEASUREMENT
    assert sensor.native_value == -0.1278


async def test_gps_accuracy_sensor(hass, mock_device):
    """Test GPS accuracy sensor."""
    coordinator = MagicMock()
    coordinator.data = {"devices": [mock_device]}

    description = next(d for d in SENSOR_DESCRIPTIONS if d.key == "gps_accuracy")
    sensor = PetTracerSensor(coordinator, mock_device, description)

    assert sensor.unique_id == "pettracer_12345_gps_accuracy"
    assert sensor.name == "Fluffy GPS Accuracy"
    assert sensor.device_class == SensorDeviceClass.DISTANCE
    assert sensor.native_unit_of_measurement == "m"
    assert sensor.state_class == SensorStateClass.MEASUREMENT
    assert sensor.entity_category == EntityCategory.DIAGNOSTIC
    assert sensor.native_value == 10


async def test_last_contact_sensor(hass, mock_device):
    """Test last contact sensor."""
    from datetime import datetime

    coordinator = MagicMock()
    coordinator.data = {"devices": [mock_device]}

    description = next(d for d in SENSOR_DESCRIPTIONS if d.key == "last_contact")
    sensor = PetTracerSensor(coordinator, mock_device, description)

    assert sensor.unique_id == "pettracer_12345_last_contact"
    assert sensor.name == "Fluffy Last Contact"
    assert sensor.device_class == SensorDeviceClass.TIMESTAMP
    assert sensor.native_value == datetime(2026, 1, 11, 10, 30, 0)


async def test_satellites_sensor(hass, mock_device):
    """Test satellites sensor."""
    coordinator = MagicMock()
    coordinator.data = {"devices": [mock_device]}

    description = next(d for d in SENSOR_DESCRIPTIONS if d.key == "satellites")
    sensor = PetTracerSensor(coordinator, mock_device, description)

    assert sensor.unique_id == "pettracer_12345_satellites"
    assert sensor.name == "Fluffy Satellites"
    assert sensor.state_class == SensorStateClass.MEASUREMENT
    assert sensor.entity_category == EntityCategory.DIAGNOSTIC
    assert sensor.native_value == 8


async def test_signal_strength_sensor(hass, mock_device):
    """Test signal strength sensor."""
    coordinator = MagicMock()
    coordinator.data = {"devices": [mock_device]}

    description = next(d for d in SENSOR_DESCRIPTIONS if d.key == "signal_strength")
    sensor = PetTracerSensor(coordinator, mock_device, description)

    assert sensor.unique_id == "pettracer_12345_signal_strength"
    assert sensor.name == "Fluffy Signal Strength"
    assert sensor.device_class == SensorDeviceClass.SIGNAL_STRENGTH
    assert sensor.native_unit_of_measurement == "dBm"
    assert sensor.state_class == SensorStateClass.MEASUREMENT
    assert sensor.entity_category == EntityCategory.DIAGNOSTIC
    assert sensor.native_value == -65


async def test_position_time_sensor(hass, mock_device):
    """Test position time sensor."""
    coordinator = MagicMock()
    coordinator.data = {"devices": [mock_device]}

    description = next(d for d in SENSOR_DESCRIPTIONS if d.key == "position_time")
    sensor = PetTracerSensor(coordinator, mock_device, description)

    assert sensor.unique_id == "pettracer_12345_position_time"
    assert sensor.name == "Fluffy Position Time"
    assert sensor.device_class == SensorDeviceClass.TIMESTAMP
    # The value should be parsed from the mock device's timeMeasure
    assert sensor.native_value is not None


async def test_status_sensor(hass, mock_device):
    """Test status sensor."""
    coordinator = MagicMock()
    coordinator.data = {"devices": [mock_device]}

    description = next(d for d in SENSOR_DESCRIPTIONS if d.key == "status")
    sensor = PetTracerSensor(coordinator, mock_device, description)

    assert sensor.unique_id == "pettracer_12345_status"
    assert sensor.name == "Fluffy Status"
    assert sensor.entity_category == EntityCategory.DIAGNOSTIC
    assert sensor.native_value == 0


async def test_mode_sensor(hass, mock_device):
    """Test mode sensor."""
    coordinator = MagicMock()
    coordinator.data = {"devices": [mock_device]}

    description = next(d for d in SENSOR_DESCRIPTIONS if d.key == "mode")
    sensor = PetTracerSensor(coordinator, mock_device, description)

    assert sensor.unique_id == "pettracer_12345_mode"
    assert sensor.name == "Fluffy Mode"
    assert sensor.native_value == "Fast"
    assert sensor.extra_state_attributes == {"mode_number": 1}


async def test_mode_sensor_all_modes(hass, mock_device):
    """Test mode sensor with all valid mode values."""
    from custom_components.pettracer.const import (
        MODE_LIVE,
        MODE_FAST_PLUS,
        MODE_FAST,
        MODE_NORMAL_PLUS,
        MODE_NORMAL,
        MODE_SLOW_PLUS,
        MODE_SLOW,
    )

    coordinator = MagicMock()

    description = next(d for d in SENSOR_DESCRIPTIONS if d.key == "mode")
    sensor = PetTracerSensor(coordinator, mock_device, description)

    # Test all mode mappings
    test_cases = [
        (MODE_LIVE, "Live"),
        (MODE_FAST_PLUS, "Fast+"),
        (MODE_FAST, "Fast"),
        (MODE_NORMAL_PLUS, "Normal+"),
        (MODE_NORMAL, "Normal"),
        (MODE_SLOW_PLUS, "Slow+"),
        (MODE_SLOW, "Slow"),
    ]

    for mode_value, mode_name in test_cases:
        mock_device.mode = mode_value
        coordinator.data = {"devices": [mock_device]}

        assert sensor.native_value == mode_name
        assert sensor.extra_state_attributes == {"mode_number": mode_value}


async def test_mode_sensor_unrecognized(hass, mock_device):
    """Test mode sensor with unrecognized mode value."""
    coordinator = MagicMock()

    description = next(d for d in SENSOR_DESCRIPTIONS if d.key == "mode")
    sensor = PetTracerSensor(coordinator, mock_device, description)

    # Set an unrecognized mode value
    mock_device.mode = 999
    coordinator.data = {"devices": [mock_device]}

    assert sensor.native_value == "Unrecognized"
    assert sensor.extra_state_attributes == {"mode_number": 999}


async def test_sensor_no_position(hass, mock_device_no_position):
    """Test sensors with no position data."""
    coordinator = MagicMock()
    coordinator.data = {"devices": [mock_device_no_position]}

    for key in ("latitude", "longitude", "gps_accuracy", "satellites", "signal_strength", "position_time"):
        description = next(d for d in SENSOR_DESCRIPTIONS if d.key == key)
        sensor = PetTracerSensor(coordinator, mock_device_no_position, description)
        assert sensor.native_value is None


async def test_sensor_device_info(hass, mock_device):
    """Test sensor device info."""
    coordinator = MagicMock()
    coordinator.data = {"devices": [mock_device]}

    description = next(d for d in SENSOR_DESCRIPTIONS if d.key == "battery_level")
    sensor = PetTracerSensor(coordinator, mock_device, description)
    device_info = sensor.device_info

    assert device_info["identifiers"] == {(DOMAIN, 12345)}
    assert device_info["name"] == "Fluffy"
    assert device_info["manufacturer"] == "PetTracer"
    assert device_info["model"] == "GPS Collar"
    assert device_info["sw_version"] == 656393


async def test_sensor_coordinator_update(hass, mock_device):
    """Test sensor updates from coordinator."""
    coordinator = MagicMock()
    coordinator.data = {"devices": [mock_device]}

    description = next(d for d in SENSOR_DESCRIPTIONS if d.key == "latitude")
    sensor = PetTracerSensor(coordinator, mock_device, description)

    # Initial value
    assert sensor.native_value == 51.5074

    # Update device position
    mock_device.lastPos.posLat = 51.5100
    coordinator.data = {"devices": [mock_device]}

    # Value should update
    assert sensor.native_value == 51.5100


async def test_multiple_devices_sensors(hass, mock_device, mock_device_no_position):
    """Test sensors with multiple devices."""
    coordinator = MagicMock()
    coordinator.data = {"devices": [mock_device, mock_device_no_position]}

    description = next(d for d in SENSOR_DESCRIPTIONS if d.key == "battery_level")
    sensor1 = PetTracerSensor(coordinator, mock_device, description)
    sensor2 = PetTracerSensor(coordinator, mock_device_no_position, description)

    assert sensor1.unique_id == "pettracer_12345_battery_level"
    assert sensor2.unique_id == "pettracer_12346_battery_level"
    assert sensor1.name == "Fluffy Battery Level"
    assert sensor2.name == "Rex Battery Level"


async def test_sensor_no_details(hass):
    """Test sensor when device has no details."""
    device = MagicMock()
    device.id = 99999
    device.details = None
    device.bat = None
    device.lastPos = None
    device.sw = None

    coordinator = MagicMock()
    coordinator.data = {"devices": [device]}

    description = next(d for d in SENSOR_DESCRIPTIONS if d.key == "battery_level")
    sensor = PetTracerSensor(coordinator, device, description)

    assert sensor.unique_id == "pettracer_99999_battery_level"
    assert sensor.name == "PetTracer 99999 Battery Level"
    assert sensor.native_value is None

    device_info = sensor.device_info
    assert device_info["sw_version"] is None


async def test_battery_percentage_edge_cases(hass, mock_device):
    """Test battery percentage calculation with edge cases."""
    coordinator = MagicMock()
    coordinator.data = {"devices": [mock_device]}

    description = next(d for d in SENSOR_DESCRIPTIONS if d.key == "battery_level")
    sensor = PetTracerSensor(coordinator, mock_device, description)

    # Test minimum voltage (3600mV = 0%)
    mock_device.bat = 3600
    assert sensor.native_value == 0

    # Test maximum voltage (4200mV = 100%)
    mock_device.bat = 4200
    assert sensor.native_value == 100

    # Test below minimum (should cap at 0%)
    mock_device.bat = 3500
    assert sensor.native_value == 0

    # Test above maximum (should cap at 100%)
    mock_device.bat = 4300
    assert sensor.native_value == 100

    # Test mid-range (3900mV = 50%)
    mock_device.bat = 3900
    assert sensor.native_value == 50

    # Test 3800mV (should be 33%)
    mock_device.bat = 3800
    assert sensor.native_value == 33

    # Test 4000mV (should be 66%)
    mock_device.bat = 4000
    assert sensor.native_value == 66

    # Test 4100mV (should be 83%)
    mock_device.bat = 4100
    assert sensor.native_value == 83
