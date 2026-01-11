"""Tests for the PetTracer integration init."""
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from pettracer import PetTracerError
from pytest_homeassistant_custom_component.common import MockConfigEntry

from homeassistant.config_entries import ConfigEntry, ConfigEntryState
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.exceptions import ConfigEntryAuthFailed, ConfigEntryNotReady

from custom_components.pettracer.const import DOMAIN


async def test_setup_entry_success(hass, mock_pettracer_client_init, mock_device):
    """Test successful setup of a config entry."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={
            CONF_USERNAME: "test@example.com",
            CONF_PASSWORD: "test_password",
        },
        entry_id="test_entry",
    )
    entry.add_to_hass(hass)
    
    mock_pettracer_client_init.get_all_devices.return_value = [mock_device]
    
    with patch("custom_components.pettracer.PetTracerClient") as mock_client:
        mock_client.return_value = mock_pettracer_client_init
        
        with patch(
            "homeassistant.config_entries.ConfigEntries.async_forward_entry_setups"
        ) as mock_forward:
            mock_forward.return_value = True
            
            # Note: The actual setup happens in async_setup_entry which we need to import
            from custom_components.pettracer import async_setup_entry
            
            result = await async_setup_entry(hass, entry)
            
            assert result is True
            assert DOMAIN in hass.data
            assert entry.entry_id in hass.data[DOMAIN]


async def test_setup_entry_auth_failed(hass, mock_pettracer_client_init):
    """Test setup fails with authentication error."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={
            CONF_USERNAME: "test@example.com",
            CONF_PASSWORD: "wrong_password",
        },
        entry_id="test_entry",
    )
    entry.add_to_hass(hass)
    
    mock_pettracer_client_init.login.side_effect = PetTracerError("Invalid credentials")
    
    with patch("custom_components.pettracer.PetTracerClient") as mock_client:
        mock_client.return_value = mock_pettracer_client_init
        
        from custom_components.pettracer import async_setup_entry
        
        with pytest.raises(ConfigEntryAuthFailed):
            await async_setup_entry(hass, entry)


async def test_setup_entry_not_ready(hass, mock_pettracer_client_init):
    """Test setup fails with unexpected error."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={
            CONF_USERNAME: "test@example.com",
            CONF_PASSWORD: "test_password",
        },
        entry_id="test_entry",
    )
    entry.add_to_hass(hass)
    
    mock_pettracer_client_init.login.side_effect = Exception("Network error")
    
    with patch("custom_components.pettracer.PetTracerClient") as mock_client:
        mock_client.return_value = mock_pettracer_client_init
        
        from custom_components.pettracer import async_setup_entry
        
        with pytest.raises(ConfigEntryNotReady):
            await async_setup_entry(hass, entry)


async def test_unload_entry(hass, mock_pettracer_client_init, mock_device):
    """Test unloading a config entry."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={
            CONF_USERNAME: "test@example.com",
            CONF_PASSWORD: "test_password",
        },
        entry_id="test_entry",
    )
    entry.add_to_hass(hass)
    
    mock_pettracer_client_init.get_all_devices.return_value = [mock_device]
    
    with patch("custom_components.pettracer.PetTracerClient") as mock_client:
        mock_client.return_value = mock_pettracer_client_init
        
        from custom_components.pettracer import async_setup_entry, async_unload_entry
        
        # Setup first
        with patch(
            "homeassistant.config_entries.ConfigEntries.async_forward_entry_setups"
        ):
            await async_setup_entry(hass, entry)
        
        # Now unload
        with patch(
            "homeassistant.config_entries.ConfigEntries.async_unload_platforms",
            return_value=True,
        ):
            result = await async_unload_entry(hass, entry)
            
            assert result is True
            assert entry.entry_id not in hass.data[DOMAIN]


async def test_coordinator_update_success(hass, mock_pettracer_client_init, mock_device):
    """Test coordinator successfully fetches data."""
    from custom_components.pettracer import PetTracerDataUpdateCoordinator
    
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
    
    coordinator = PetTracerDataUpdateCoordinator(hass, mock_pettracer_client_init, entry)
    
    await coordinator.async_config_entry_first_refresh()
    
    assert coordinator.data is not None
    assert "devices" in coordinator.data
    assert len(coordinator.data["devices"]) == 1
    assert coordinator.data["devices"][0].id == 12345


async def test_coordinator_update_failure(hass, mock_pettracer_client_init):
    """Test coordinator handles API errors."""
    from custom_components.pettracer import PetTracerDataUpdateCoordinator
    
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
    
    mock_pettracer_client_init.get_all_devices.side_effect = PetTracerError("API Error")
    
    coordinator = PetTracerDataUpdateCoordinator(hass, mock_pettracer_client_init, entry)
    
    # async_config_entry_first_refresh converts UpdateFailed to ConfigEntryNotReady during setup
    with pytest.raises(ConfigEntryNotReady):
        await coordinator.async_config_entry_first_refresh()


async def test_coordinator_multiple_devices(hass, mock_pettracer_client_init, mock_device, mock_device_no_position):
    """Test coordinator handles multiple devices."""
    from custom_components.pettracer import PetTracerDataUpdateCoordinator
    
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
    
    mock_pettracer_client_init.get_all_devices.return_value = [mock_device, mock_device_no_position]
    
    coordinator = PetTracerDataUpdateCoordinator(hass, mock_pettracer_client_init, entry)
    
    await coordinator.async_config_entry_first_refresh()
    
    assert coordinator.data is not None
    assert "devices" in coordinator.data
    assert len(coordinator.data["devices"]) == 2
    assert coordinator.data["devices"][0].id == 12345
    assert coordinator.data["devices"][1].id == 12346


async def test_coordinator_empty_devices(hass, mock_pettracer_client_init):
    """Test coordinator handles no devices."""
    from custom_components.pettracer import PetTracerDataUpdateCoordinator
    
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
    
    mock_pettracer_client_init.get_all_devices.return_value = []
    
    coordinator = PetTracerDataUpdateCoordinator(hass, mock_pettracer_client_init, entry)
    
    await coordinator.async_config_entry_first_refresh()
    
    assert coordinator.data is not None
    assert "devices" in coordinator.data
    assert len(coordinator.data["devices"]) == 0
