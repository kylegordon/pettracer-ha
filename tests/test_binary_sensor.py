"""Tests for the PetTracer binary sensor platform."""

from unittest.mock import MagicMock, patch

from pytest_homeassistant_custom_component.common import MockConfigEntry

from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.config_entries import ConfigEntryState
from homeassistant.components.binary_sensor import BinarySensorDeviceClass

from custom_components.pettracer.const import DOMAIN
from custom_components.pettracer.binary_sensor import (
    PetTracerAtHomeBinarySensor,
    PetTracerChargingBinarySensor,
)


async def test_binary_sensor_setup(hass, mock_pettracer_client_init, mock_device):
    """Test binary sensor entities are created."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={
            CONF_USERNAME: "test@example.com",
            CONF_PASSWORD: "test_password",
        },
        entry_id="test_entry",
    )
    entry.add_to_hass(hass)

    entry._async_set_state(hass, ConfigEntryState.SETUP_IN_PROGRESS, None)

    mock_pettracer_client_init.get_all_devices.return_value = [mock_device]

    with patch("custom_components.pettracer.PetTracerClient") as mock_client:
        mock_client.return_value = mock_pettracer_client_init

        from custom_components.pettracer import async_setup_entry
        from custom_components.pettracer.binary_sensor import (
            async_setup_entry as binary_sensor_setup,
        )

        with patch(
            "homeassistant.config_entries.ConfigEntries.async_forward_entry_setups"
        ):
            await async_setup_entry(hass, entry)

        entities = []

        def mock_add_entities(new_entities, update_before_add):
            entities.extend(new_entities)

        await binary_sensor_setup(hass, entry, mock_add_entities)

        assert len(entities) == 2
        assert isinstance(entities[0], PetTracerAtHomeBinarySensor)
        assert isinstance(entities[1], PetTracerChargingBinarySensor)


async def test_at_home_binary_sensor_true(hass, mock_device):
    """Test at home binary sensor when pet is home."""
    coordinator = MagicMock()
    coordinator.data = {"devices": [mock_device]}

    sensor = PetTracerAtHomeBinarySensor(coordinator, mock_device)

    assert sensor.unique_id == "pettracer_12345_at_home"
    assert sensor.name == "Fluffy At Home"
    assert sensor.device_class == BinarySensorDeviceClass.PRESENCE
    assert sensor.is_on is True


async def test_at_home_binary_sensor_false(hass, mock_device_no_position):
    """Test at home binary sensor when pet is not home."""
    coordinator = MagicMock()
    coordinator.data = {"devices": [mock_device_no_position]}

    sensor = PetTracerAtHomeBinarySensor(coordinator, mock_device_no_position)

    assert sensor.unique_id == "pettracer_12346_at_home"
    assert sensor.name == "Rex At Home"
    assert sensor.is_on is False


async def test_at_home_binary_sensor_none(hass):
    """Test at home binary sensor when home status is None."""
    device = MagicMock()
    device.id = 99999
    device.details = None
    device.home = None
    device.sw = None

    coordinator = MagicMock()
    coordinator.data = {"devices": [device]}

    sensor = PetTracerAtHomeBinarySensor(coordinator, device)

    assert sensor.is_on is None


async def test_at_home_binary_sensor_device_info(hass, mock_device):
    """Test at home binary sensor device info."""
    coordinator = MagicMock()
    coordinator.data = {"devices": [mock_device]}

    sensor = PetTracerAtHomeBinarySensor(coordinator, mock_device)
    device_info = sensor.device_info

    assert device_info["identifiers"] == {(DOMAIN, 12345)}
    assert device_info["name"] == "Fluffy"
    assert device_info["manufacturer"] == "PetTracer"
    assert device_info["model"] == "GPS Collar"


async def test_charging_binary_sensor_true(hass, mock_device):
    """Test charging binary sensor when collar is charging."""
    coordinator = MagicMock()
    coordinator.data = {"devices": [mock_device]}

    sensor = PetTracerChargingBinarySensor(coordinator, mock_device)

    assert sensor.unique_id == "pettracer_12345_charging"
    assert sensor.name == "Fluffy Charging"
    assert sensor.device_class == BinarySensorDeviceClass.BATTERY_CHARGING
    assert sensor.is_on is True


async def test_charging_binary_sensor_false(hass, mock_device_no_position):
    """Test charging binary sensor when collar is not charging."""
    coordinator = MagicMock()
    coordinator.data = {"devices": [mock_device_no_position]}

    sensor = PetTracerChargingBinarySensor(coordinator, mock_device_no_position)

    assert sensor.unique_id == "pettracer_12346_charging"
    assert sensor.name == "Rex Charging"
    assert sensor.is_on is False


async def test_charging_binary_sensor_none(hass):
    """Test charging binary sensor when chg is None."""
    device = MagicMock()
    device.id = 99999
    device.details = None
    device.chg = None
    device.sw = None

    coordinator = MagicMock()
    coordinator.data = {"devices": [device]}

    sensor = PetTracerChargingBinarySensor(coordinator, device)

    assert sensor.is_on is None


async def test_charging_binary_sensor_device_info(hass, mock_device):
    """Test charging binary sensor device info."""
    coordinator = MagicMock()
    coordinator.data = {"devices": [mock_device]}

    sensor = PetTracerChargingBinarySensor(coordinator, mock_device)
    device_info = sensor.device_info

    assert device_info["identifiers"] == {(DOMAIN, 12345)}
    assert device_info["name"] == "Fluffy"
    assert device_info["manufacturer"] == "PetTracer"
    assert device_info["model"] == "GPS Collar"
