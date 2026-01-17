"""Tests for the PetTracer sensor platform."""
from unittest.mock import MagicMock, patch
from datetime import datetime

import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry

from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorStateClass,
)

from custom_components.pettracer.const import DOMAIN


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
    from homeassistant.config_entries import ConfigEntryState
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
        
        coordinator = hass.data[DOMAIN][entry.entry_id]
        
        # Setup sensor platform
        entities = []
        
        def mock_add_entities(new_entities, update_before_add):
            entities.extend(new_entities)
        
        await sensor_setup(hass, entry, mock_add_entities)
        
        # Should create 12 sensors per device
        assert len(entities) == 12
        
        # Check sensor types
        sensor_types = [type(e).__name__ for e in entities]
        assert "PetTracerBatterySensor" in sensor_types
        assert "PetTracerBatteryVoltageSensor" in sensor_types
        assert "PetTracerLatitudeSensor" in sensor_types
        assert "PetTracerLongitudeSensor" in sensor_types
        assert "PetTracerGPSAccuracySensor" in sensor_types
        assert "PetTracerLastContactSensor" in sensor_types
        assert "PetTracerSatellitesSensor" in sensor_types
        assert "PetTracerSignalStrengthSensor" in sensor_types
        assert "PetTracerPositionTimeSensor" in sensor_types
        assert "PetTracerStatusSensor" in sensor_types
        assert "PetTracerModeSensor" in sensor_types
        assert "PetTracerAtHomeSensor" in sensor_types


async def test_battery_sensor(hass, mock_device):
    """Test battery level sensor."""
    from custom_components.pettracer.sensor import PetTracerBatterySensor
    
    coordinator = MagicMock()
    coordinator.data = {"devices": [mock_device]}
    
    sensor = PetTracerBatterySensor(coordinator, mock_device)
    
    assert sensor.unique_id == "pettracer_12345_battery_level"
    assert sensor.name == "Fluffy Battery Level"
    assert sensor.device_class == SensorDeviceClass.BATTERY
    assert sensor.native_unit_of_measurement == "%"
    assert sensor.state_class == SensorStateClass.MEASUREMENT
    
    # Test battery conversion (4100mV should be around 91%)
    battery = sensor.native_value
    assert battery is not None
    assert 80 <= battery <= 95


async def test_battery_voltage_sensor(hass, mock_device):
    """Test battery voltage sensor."""
    from custom_components.pettracer.sensor import PetTracerBatteryVoltageSensor
    
    coordinator = MagicMock()
    coordinator.data = {"devices": [mock_device]}
    
    sensor = PetTracerBatteryVoltageSensor(coordinator, mock_device)
    
    assert sensor.unique_id == "pettracer_12345_battery_voltage"
    assert sensor.name == "Fluffy Battery Voltage"
    assert sensor.device_class == SensorDeviceClass.VOLTAGE
    assert sensor.native_unit_of_measurement == "mV"
    assert sensor.state_class == SensorStateClass.MEASUREMENT
    assert sensor.native_value == 4100


async def test_latitude_sensor(hass, mock_device):
    """Test latitude sensor."""
    from custom_components.pettracer.sensor import PetTracerLatitudeSensor
    
    coordinator = MagicMock()
    coordinator.data = {"devices": [mock_device]}
    
    sensor = PetTracerLatitudeSensor(coordinator, mock_device)
    
    assert sensor.unique_id == "pettracer_12345_latitude"
    assert sensor.name == "Fluffy Latitude"
    assert sensor.state_class == SensorStateClass.MEASUREMENT
    assert sensor.native_value == 51.5074


async def test_longitude_sensor(hass, mock_device):
    """Test longitude sensor."""
    from custom_components.pettracer.sensor import PetTracerLongitudeSensor
    
    coordinator = MagicMock()
    coordinator.data = {"devices": [mock_device]}
    
    sensor = PetTracerLongitudeSensor(coordinator, mock_device)
    
    assert sensor.unique_id == "pettracer_12345_longitude"
    assert sensor.name == "Fluffy Longitude"
    assert sensor.state_class == SensorStateClass.MEASUREMENT
    assert sensor.native_value == -0.1278


async def test_gps_accuracy_sensor(hass, mock_device):
    """Test GPS accuracy sensor."""
    from custom_components.pettracer.sensor import PetTracerGPSAccuracySensor
    
    coordinator = MagicMock()
    coordinator.data = {"devices": [mock_device]}
    
    sensor = PetTracerGPSAccuracySensor(coordinator, mock_device)
    
    assert sensor.unique_id == "pettracer_12345_gps_accuracy"
    assert sensor.name == "Fluffy GPS Accuracy"
    assert sensor.device_class == SensorDeviceClass.DISTANCE
    assert sensor.native_unit_of_measurement == "m"
    assert sensor.state_class == SensorStateClass.MEASUREMENT
    assert sensor.native_value == 10


async def test_last_contact_sensor(hass, mock_device):
    """Test last contact sensor."""
    from custom_components.pettracer.sensor import PetTracerLastContactSensor
    
    coordinator = MagicMock()
    coordinator.data = {"devices": [mock_device]}
    
    sensor = PetTracerLastContactSensor(coordinator, mock_device)
    
    assert sensor.unique_id == "pettracer_12345_last_contact"
    assert sensor.name == "Fluffy Last Contact"
    assert sensor.device_class == SensorDeviceClass.TIMESTAMP
    assert sensor.native_value == "2026-01-11T10:30:00"


async def test_satellites_sensor(hass, mock_device):
    """Test satellites sensor."""
    from custom_components.pettracer.sensor import PetTracerSatellitesSensor
    
    coordinator = MagicMock()
    coordinator.data = {"devices": [mock_device]}
    
    sensor = PetTracerSatellitesSensor(coordinator, mock_device)
    
    assert sensor.unique_id == "pettracer_12345_satellites"
    assert sensor.name == "Fluffy Satellites"
    assert sensor.state_class == SensorStateClass.MEASUREMENT
    assert sensor.native_value == 8


async def test_signal_strength_sensor(hass, mock_device):
    """Test signal strength sensor."""
    from custom_components.pettracer.sensor import PetTracerSignalStrengthSensor
    
    coordinator = MagicMock()
    coordinator.data = {"devices": [mock_device]}
    
    sensor = PetTracerSignalStrengthSensor(coordinator, mock_device)
    
    assert sensor.unique_id == "pettracer_12345_signal_strength"
    assert sensor.name == "Fluffy Signal Strength"
    assert sensor.device_class == SensorDeviceClass.SIGNAL_STRENGTH
    assert sensor.native_unit_of_measurement == "dBm"
    assert sensor.state_class == SensorStateClass.MEASUREMENT
    assert sensor.native_value == -65


async def test_position_time_sensor(hass, mock_device):
    """Test position time sensor."""
    from custom_components.pettracer.sensor import PetTracerPositionTimeSensor
    
    coordinator = MagicMock()
    coordinator.data = {"devices": [mock_device]}
    
    sensor = PetTracerPositionTimeSensor(coordinator, mock_device)
    
    assert sensor.unique_id == "pettracer_12345_position_time"
    assert sensor.name == "Fluffy Position Time"
    assert sensor.device_class == SensorDeviceClass.TIMESTAMP
    # The value should be parsed from the mock device's timeMeasure
    assert sensor.native_value is not None


async def test_status_sensor(hass, mock_device):
    """Test status sensor."""
    from custom_components.pettracer.sensor import PetTracerStatusSensor
    
    coordinator = MagicMock()
    coordinator.data = {"devices": [mock_device]}
    
    sensor = PetTracerStatusSensor(coordinator, mock_device)
    
    assert sensor.unique_id == "pettracer_12345_status"
    assert sensor.name == "Fluffy Status"
    assert sensor.native_value == 0


async def test_mode_sensor(hass, mock_device):
    """Test mode sensor."""
    from custom_components.pettracer.sensor import PetTracerModeSensor
    
    coordinator = MagicMock()
    coordinator.data = {"devices": [mock_device]}
    
    sensor = PetTracerModeSensor(coordinator, mock_device)
    
    assert sensor.unique_id == "pettracer_12345_mode"
    assert sensor.name == "Fluffy Mode"
    assert sensor.native_value == 1


async def test_at_home_sensor(hass, mock_device):
    """Test at home sensor."""
    from custom_components.pettracer.sensor import PetTracerAtHomeSensor
    
    coordinator = MagicMock()
    coordinator.data = {"devices": [mock_device]}
    
    sensor = PetTracerAtHomeSensor(coordinator, mock_device)
    
    assert sensor.unique_id == "pettracer_12345_at_home"
    assert sensor.name == "Fluffy At Home"
    assert sensor.native_value == "true"


async def test_sensor_no_position(hass, mock_device_no_position):
    """Test sensors with no position data."""
    from custom_components.pettracer.sensor import (
        PetTracerLatitudeSensor,
        PetTracerLongitudeSensor,
        PetTracerGPSAccuracySensor,
        PetTracerSatellitesSensor,
        PetTracerSignalStrengthSensor,
        PetTracerPositionTimeSensor,
    )
    
    coordinator = MagicMock()
    coordinator.data = {"devices": [mock_device_no_position]}
    
    lat_sensor = PetTracerLatitudeSensor(coordinator, mock_device_no_position)
    assert lat_sensor.native_value is None
    
    lon_sensor = PetTracerLongitudeSensor(coordinator, mock_device_no_position)
    assert lon_sensor.native_value is None
    
    acc_sensor = PetTracerGPSAccuracySensor(coordinator, mock_device_no_position)
    assert acc_sensor.native_value == 0
    
    sat_sensor = PetTracerSatellitesSensor(coordinator, mock_device_no_position)
    assert sat_sensor.native_value is None
    
    sig_sensor = PetTracerSignalStrengthSensor(coordinator, mock_device_no_position)
    assert sig_sensor.native_value is None
    
    pos_sensor = PetTracerPositionTimeSensor(coordinator, mock_device_no_position)
    assert pos_sensor.native_value is None


async def test_sensor_device_info(hass, mock_device):
    """Test sensor device info."""
    from custom_components.pettracer.sensor import PetTracerBatterySensor
    
    coordinator = MagicMock()
    coordinator.data = {"devices": [mock_device]}
    
    sensor = PetTracerBatterySensor(coordinator, mock_device)
    device_info = sensor.device_info
    
    assert device_info["identifiers"] == {(DOMAIN, 12345)}
    assert device_info["name"] == "Fluffy"
    assert device_info["manufacturer"] == "PetTracer"
    assert device_info["model"] == "GPS Collar"
    assert device_info["sw_version"] == 656393


async def test_sensor_coordinator_update(hass, mock_device):
    """Test sensor updates from coordinator."""
    from custom_components.pettracer.sensor import PetTracerLatitudeSensor
    
    coordinator = MagicMock()
    coordinator.data = {"devices": [mock_device]}
    
    sensor = PetTracerLatitudeSensor(coordinator, mock_device)
    
    # Initial value
    assert sensor.native_value == 51.5074
    
    # Update device position
    mock_device.lastPos.posLat = 51.5100
    coordinator.data = {"devices": [mock_device]}
    
    # Value should update
    assert sensor.native_value == 51.5100


async def test_multiple_devices_sensors(hass, mock_device, mock_device_no_position):
    """Test sensors with multiple devices."""
    from custom_components.pettracer.sensor import PetTracerBatterySensor
    
    coordinator = MagicMock()
    coordinator.data = {"devices": [mock_device, mock_device_no_position]}
    
    sensor1 = PetTracerBatterySensor(coordinator, mock_device)
    sensor2 = PetTracerBatterySensor(coordinator, mock_device_no_position)
    
    assert sensor1.unique_id == "pettracer_12345_battery_level"
    assert sensor2.unique_id == "pettracer_12346_battery_level"
    assert sensor1.name == "Fluffy Battery Level"
    assert sensor2.name == "Rex Battery Level"


async def test_sensor_no_details(hass):
    """Test sensor when device has no details."""
    from custom_components.pettracer.sensor import PetTracerBatterySensor
    
    device = MagicMock()
    device.id = 99999
    device.details = None
    device.bat = None
    device.lastPos = None
    device.sw = None
    
    coordinator = MagicMock()
    coordinator.data = {"devices": [device]}
    
    sensor = PetTracerBatterySensor(coordinator, device)
    
    assert sensor.unique_id == "pettracer_99999_battery_level"
    assert sensor.name == "PetTracer 99999 Battery Level"
    assert sensor.native_value is None
    
    device_info = sensor.device_info
    assert device_info["sw_version"] is None
