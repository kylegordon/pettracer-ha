"""Tests for the PetTracer device tracker platform."""
from unittest.mock import MagicMock, patch

import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry

from homeassistant.components.device_tracker import SourceType
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME

from custom_components.pettracer.const import DOMAIN


async def test_device_tracker_setup(hass, mock_pettracer_client_init, mock_device):
    """Test device tracker entities are created."""
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
        from custom_components.pettracer.device_tracker import async_setup_entry as tracker_setup
        
        # Setup integration
        with patch(
            "homeassistant.config_entries.ConfigEntries.async_forward_entry_setups"
        ):
            await async_setup_entry(hass, entry)
        
        coordinator = hass.data[DOMAIN][entry.entry_id]
        
        # Setup device tracker platform
        entities = []
        
        def mock_add_entities(new_entities, update_before_add):
            entities.extend(new_entities)
        
        await tracker_setup(hass, entry, mock_add_entities)
        
        assert len(entities) == 1
        assert entities[0]._device.id == 12345


async def test_device_tracker_properties(hass, mock_device):
    """Test device tracker properties."""
    from custom_components.pettracer.device_tracker import PetTracerDeviceTracker
    
    coordinator = MagicMock()
    coordinator.data = {"devices": [mock_device]}
    
    tracker = PetTracerDeviceTracker(coordinator, mock_device)
    
    assert tracker.unique_id == "pettracer_12345"
    assert tracker.name == "Fluffy"
    assert tracker.source_type == SourceType.GPS
    assert tracker.latitude == 51.5074
    assert tracker.longitude == -0.1278
    assert tracker.location_accuracy == 10


async def test_device_tracker_battery_conversion(hass, mock_device):
    """Test battery voltage to percentage conversion."""
    from custom_components.pettracer.device_tracker import PetTracerDeviceTracker
    
    coordinator = MagicMock()
    coordinator.data = {"devices": [mock_device]}
    
    # Test with 4100mV (mid-range)
    mock_device.bat = 4100
    tracker = PetTracerDeviceTracker(coordinator, mock_device)
    battery = tracker.battery_level
    assert battery is not None
    assert 80 <= battery <= 95
    
    # Test with full battery (4200mV)
    mock_device.bat = 4200
    coordinator.data = {"devices": [mock_device]}
    battery = tracker.battery_level
    assert battery == 100
    
    # Test with low battery (3000mV)
    mock_device.bat = 3000
    coordinator.data = {"devices": [mock_device]}
    battery = tracker.battery_level
    assert battery == 0
    
    # Test with very high battery (above 4200mV)
    mock_device.bat = 4500
    coordinator.data = {"devices": [mock_device]}
    battery = tracker.battery_level
    assert battery == 100


async def test_device_tracker_no_position(hass, mock_device_no_position):
    """Test device tracker with no position data."""
    from custom_components.pettracer.device_tracker import PetTracerDeviceTracker
    
    coordinator = MagicMock()
    coordinator.data = {"devices": [mock_device_no_position]}
    
    tracker = PetTracerDeviceTracker(coordinator, mock_device_no_position)
    
    assert tracker.unique_id == "pettracer_12346"
    assert tracker.name == "Rex"
    assert tracker.latitude is None
    assert tracker.longitude is None
    assert tracker.location_accuracy == 0


async def test_device_tracker_attributes(hass, mock_device):
    """Test device tracker extra state attributes."""
    from custom_components.pettracer.device_tracker import PetTracerDeviceTracker
    
    coordinator = MagicMock()
    coordinator.data = {"devices": [mock_device]}
    
    tracker = PetTracerDeviceTracker(coordinator, mock_device)
    attributes = tracker.extra_state_attributes
    
    assert "battery_voltage_mv" in attributes
    assert attributes["battery_voltage_mv"] == 4100
    assert "satellites" in attributes
    assert attributes["satellites"] == 8
    assert "signal_strength" in attributes
    assert attributes["signal_strength"] == -65
    assert "at_home" in attributes
    assert attributes["at_home"] is True
    assert "status" in attributes
    assert attributes["status"] == 0
    assert "mode" in attributes
    assert attributes["mode"] == 1


async def test_device_tracker_attributes_no_position(hass, mock_device_no_position):
    """Test device tracker attributes without position data."""
    from custom_components.pettracer.device_tracker import PetTracerDeviceTracker
    
    coordinator = MagicMock()
    coordinator.data = {"devices": [mock_device_no_position]}
    
    tracker = PetTracerDeviceTracker(coordinator, mock_device_no_position)
    attributes = tracker.extra_state_attributes
    
    assert "battery_voltage_mv" in attributes
    assert "satellites" not in attributes
    assert "signal_strength" not in attributes
    assert "position_time" not in attributes
    assert "at_home" in attributes
    assert attributes["at_home"] is False


async def test_device_tracker_device_info(hass, mock_device):
    """Test device tracker device info."""
    from custom_components.pettracer.device_tracker import PetTracerDeviceTracker
    
    coordinator = MagicMock()
    coordinator.data = {"devices": [mock_device]}
    
    tracker = PetTracerDeviceTracker(coordinator, mock_device)
    device_info = tracker.device_info
    
    assert device_info["identifiers"] == {(DOMAIN, 12345)}
    assert device_info["name"] == "Fluffy"
    assert device_info["manufacturer"] == "PetTracer"
    assert device_info["model"] == "GPS Collar"
    assert device_info["sw_version"] == 656393


async def test_device_tracker_multiple_devices(hass, mock_device, mock_device_no_position):
    """Test multiple device trackers."""
    from custom_components.pettracer.device_tracker import PetTracerDeviceTracker
    
    coordinator = MagicMock()
    coordinator.data = {"devices": [mock_device, mock_device_no_position]}
    
    tracker1 = PetTracerDeviceTracker(coordinator, mock_device)
    tracker2 = PetTracerDeviceTracker(coordinator, mock_device_no_position)
    
    assert tracker1.unique_id == "pettracer_12345"
    assert tracker2.unique_id == "pettracer_12346"
    assert tracker1.name == "Fluffy"
    assert tracker2.name == "Rex"
    assert tracker1.latitude == 51.5074
    assert tracker2.latitude is None


async def test_device_tracker_coordinator_update(hass, mock_device):
    """Test device tracker updates from coordinator."""
    from custom_components.pettracer.device_tracker import PetTracerDeviceTracker
    
    coordinator = MagicMock()
    coordinator.data = {"devices": [mock_device]}
    
    tracker = PetTracerDeviceTracker(coordinator, mock_device)
    
    # Initial values
    assert tracker.latitude == 51.5074
    assert tracker.longitude == -0.1278
    
    # Update device position
    mock_device.lastPos.posLat = 51.5100
    mock_device.lastPos.posLong = -0.1300
    coordinator.data = {"devices": [mock_device]}
    
    # Values should update
    assert tracker.latitude == 51.5100
    assert tracker.longitude == -0.1300


async def test_device_tracker_no_details(hass):
    """Test device tracker when device has no details."""
    from custom_components.pettracer.device_tracker import PetTracerDeviceTracker
    
    device = MagicMock()
    device.id = 99999
    device.details = None
    device.bat = None
    device.lastPos = None
    device.sw = None
    
    coordinator = MagicMock()
    coordinator.data = {"devices": [device]}
    
    tracker = PetTracerDeviceTracker(coordinator, device)
    
    assert tracker.unique_id == "pettracer_99999"
    assert tracker.name == "PetTracer 99999"
    assert tracker.latitude is None
    assert tracker.longitude is None
    assert tracker.battery_level is None
    
    device_info = tracker.device_info
    assert device_info["sw_version"] is None


async def test_device_tracker_partial_attributes(hass):
    """Test device tracker with partial attribute data."""
    from custom_components.pettracer.device_tracker import PetTracerDeviceTracker
    
    device = MagicMock()
    device.id = 88888
    device.bat = 4000
    device.status = None
    device.mode = None
    device.home = None
    device.sw = None
    device.lastContact = None
    
    device.details = MagicMock()
    device.details.name = "Partial"
    
    device.lastPos = MagicMock()
    device.lastPos.posLat = 50.0
    device.lastPos.posLong = -1.0
    device.lastPos.acc = 15
    device.lastPos.sat = None
    device.lastPos.rssi = None
    device.lastPos.timeMeasure = None
    
    coordinator = MagicMock()
    coordinator.data = {"devices": [device]}
    
    tracker = PetTracerDeviceTracker(coordinator, device)
    attributes = tracker.extra_state_attributes
    
    assert "battery_voltage_mv" in attributes
    assert "satellites" not in attributes
    assert "signal_strength" not in attributes
    assert "position_time" not in attributes
    assert "status" not in attributes
    assert "mode" not in attributes
    assert "at_home" not in attributes
