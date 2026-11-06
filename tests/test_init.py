"""Tests for the PetTracer integration init."""
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from pettracer import PetTracerError
from pytest_homeassistant_custom_component.common import MockConfigEntry

from homeassistant.config_entries import SOURCE_REAUTH, ConfigEntry, ConfigEntryState
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.exceptions import ConfigEntryAuthFailed, ConfigEntryNotReady
from homeassistant.helpers.update_coordinator import UpdateFailed

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
    
    # Set the entry state to SETUP_IN_PROGRESS to allow async_config_entry_first_refresh
    entry._async_set_state(hass, ConfigEntryState.SETUP_IN_PROGRESS, None)
    
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


async def test_setup_entry_auth_failed(hass, mock_pettracer_client_init, pettracer_error):
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
    
    mock_pettracer_client_init.login.side_effect = pettracer_error(401)
    
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
    
    # Set the entry state to SETUP_IN_PROGRESS to allow async_config_entry_first_refresh
    entry._async_set_state(hass, ConfigEntryState.SETUP_IN_PROGRESS, None)
    
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


def _entry(hass):
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={CONF_USERNAME: "test@example.com", CONF_PASSWORD: "test_password"},
        entry_id="test_entry",
    )
    entry.add_to_hass(hass)
    return entry


@pytest.mark.parametrize("status", [None, 500])
async def test_setup_entry_login_network_error_not_ready(
    hass, mock_pettracer_client_init, pettracer_error, status
):
    """A login outage retries setup instead of asking for new credentials."""
    entry = _entry(hass)
    mock_pettracer_client_init.login.side_effect = pettracer_error(status)

    with patch("custom_components.pettracer.PetTracerClient") as mock_client:
        mock_client.return_value = mock_pettracer_client_init
        from custom_components.pettracer import async_setup_entry

        with pytest.raises(ConfigEntryNotReady):
            await async_setup_entry(hass, entry)


async def test_coordinator_relogin_on_expired_token(
    hass, mock_pettracer_client_init, mock_device, pettracer_error
):
    """A 403 on poll logs in again with the stored credentials and retries."""
    from custom_components.pettracer import PetTracerDataUpdateCoordinator

    entry = _entry(hass)
    mock_pettracer_client_init.get_all_devices.side_effect = [
        pettracer_error(403),
        [mock_device],
    ]
    coordinator = PetTracerDataUpdateCoordinator(hass, mock_pettracer_client_init, entry)

    data = await coordinator._async_update_data()

    assert data == {"devices": [mock_device]}
    mock_pettracer_client_init.login.assert_awaited_once_with(
        "test@example.com", "test_password"
    )
    assert mock_pettracer_client_init.get_all_devices.await_count == 2


async def test_coordinator_relogin_rejected_starts_reauth(
    hass, mock_pettracer_client_init, pettracer_error
):
    """If the re-login is refused, the coordinator raises ConfigEntryAuthFailed."""
    from custom_components.pettracer import PetTracerDataUpdateCoordinator

    entry = _entry(hass)
    mock_pettracer_client_init.get_all_devices.side_effect = pettracer_error(403)
    mock_pettracer_client_init.login.side_effect = pettracer_error(401)
    coordinator = PetTracerDataUpdateCoordinator(hass, mock_pettracer_client_init, entry)

    with pytest.raises(ConfigEntryAuthFailed):
        await coordinator._async_update_data()
    assert mock_pettracer_client_init.get_all_devices.await_count == 1


async def test_coordinator_relogin_network_error_is_update_failed(
    hass, mock_pettracer_client_init, pettracer_error
):
    """A network failure during re-login is a normal update failure, not reauth."""
    from custom_components.pettracer import PetTracerDataUpdateCoordinator

    entry = _entry(hass)
    mock_pettracer_client_init.get_all_devices.side_effect = pettracer_error(403)
    mock_pettracer_client_init.login.side_effect = pettracer_error()
    coordinator = PetTracerDataUpdateCoordinator(hass, mock_pettracer_client_init, entry)

    with pytest.raises(UpdateFailed):
        await coordinator._async_update_data()
    assert mock_pettracer_client_init.get_all_devices.await_count == 1


async def test_coordinator_retry_still_rejected_starts_reauth(
    hass, mock_pettracer_client_init, pettracer_error
):
    """A fresh token that is still refused raises ConfigEntryAuthFailed (no loop)."""
    from custom_components.pettracer import PetTracerDataUpdateCoordinator

    entry = _entry(hass)
    mock_pettracer_client_init.get_all_devices.side_effect = [
        pettracer_error(403),
        pettracer_error(403),
    ]
    coordinator = PetTracerDataUpdateCoordinator(hass, mock_pettracer_client_init, entry)

    with pytest.raises(ConfigEntryAuthFailed):
        await coordinator._async_update_data()
    mock_pettracer_client_init.login.assert_awaited_once()


async def test_coordinator_retry_network_error_is_update_failed(
    hass, mock_pettracer_client_init, pettracer_error
):
    """A network failure on the retry after re-login is UpdateFailed."""
    from custom_components.pettracer import PetTracerDataUpdateCoordinator

    entry = _entry(hass)
    mock_pettracer_client_init.get_all_devices.side_effect = [
        pettracer_error(403),
        pettracer_error(),
    ]
    coordinator = PetTracerDataUpdateCoordinator(hass, mock_pettracer_client_init, entry)

    with pytest.raises(UpdateFailed):
        await coordinator._async_update_data()


async def test_coordinator_network_error_does_not_relogin(
    hass, mock_pettracer_client_init, pettracer_error
):
    """Network errors on poll are UpdateFailed without a login attempt."""
    from custom_components.pettracer import PetTracerDataUpdateCoordinator

    entry = _entry(hass)
    mock_pettracer_client_init.get_all_devices.side_effect = pettracer_error()
    coordinator = PetTracerDataUpdateCoordinator(hass, mock_pettracer_client_init, entry)

    with pytest.raises(UpdateFailed):
        await coordinator._async_update_data()
    mock_pettracer_client_init.login.assert_not_awaited()


# --- Through HA's real setup / refresh path -------------------------------


def _reauth_flows(hass, entry):
    return list(entry.async_get_active_flows(hass, {SOURCE_REAUTH}))


async def _setup(hass, entry, client):
    """Set the entry up for real, with platforms stubbed out."""
    with (
        patch("custom_components.pettracer.PetTracerClient", return_value=client),
        patch(
            "homeassistant.config_entries.ConfigEntries.async_forward_entry_setups",
            return_value=True,
        ),
    ):
        await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()


async def test_real_setup_bad_password_starts_reauth(
    hass, mock_pettracer_client_init, pettracer_error
):
    """A 401 on setup login leaves the entry in SETUP_ERROR with a reauth flow."""
    entry = _entry(hass)
    mock_pettracer_client_init.login.side_effect = pettracer_error(401)

    await _setup(hass, entry, mock_pettracer_client_init)

    assert entry.state is ConfigEntryState.SETUP_ERROR
    assert len(_reauth_flows(hass, entry)) == 1


@pytest.mark.parametrize("status", [None, 500])
async def test_real_setup_outage_retries_without_reauth(
    hass, mock_pettracer_client_init, pettracer_error, status
):
    """An outage on setup login leaves the entry in SETUP_RETRY with no reauth."""
    entry = _entry(hass)
    mock_pettracer_client_init.login.side_effect = pettracer_error(status)

    await _setup(hass, entry, mock_pettracer_client_init)

    assert entry.state is ConfigEntryState.SETUP_RETRY
    assert _reauth_flows(hass, entry) == []


async def test_real_first_refresh_rejected_token_starts_reauth(
    hass, mock_pettracer_client_init, pettracer_error
):
    """Login OK but the token is refused even after re-login: SETUP_ERROR + reauth."""
    entry = _entry(hass)
    mock_pettracer_client_init.get_all_devices.side_effect = pettracer_error(403)

    await _setup(hass, entry, mock_pettracer_client_init)

    assert entry.state is ConfigEntryState.SETUP_ERROR
    assert len(_reauth_flows(hass, entry)) == 1


async def test_real_refresh_expired_token_recovers(
    hass, mock_pettracer_client_init, mock_device, pettracer_error
):
    """A loaded entry whose token expires logs in again and keeps updating."""
    entry = _entry(hass)
    mock_pettracer_client_init.get_all_devices.return_value = [mock_device]
    await _setup(hass, entry, mock_pettracer_client_init)
    assert entry.state is ConfigEntryState.LOADED
    coordinator = hass.data[DOMAIN][entry.entry_id]

    mock_pettracer_client_init.get_all_devices.side_effect = [
        pettracer_error(403),
        [mock_device],
    ]
    await coordinator.async_refresh()
    await hass.async_block_till_done()

    assert coordinator.last_update_success is True
    assert mock_pettracer_client_init.login.await_count == 2
    assert _reauth_flows(hass, entry) == []


async def test_real_refresh_password_changed_starts_reauth(
    hass, mock_pettracer_client_init, mock_device, pettracer_error
):
    """A loaded entry whose re-login is refused starts a reauth flow."""
    entry = _entry(hass)
    mock_pettracer_client_init.get_all_devices.return_value = [mock_device]
    await _setup(hass, entry, mock_pettracer_client_init)
    coordinator = hass.data[DOMAIN][entry.entry_id]

    mock_pettracer_client_init.get_all_devices.side_effect = pettracer_error(403)
    mock_pettracer_client_init.login.side_effect = pettracer_error(401)
    await coordinator.async_refresh()
    await hass.async_block_till_done()

    assert coordinator.last_update_success is False
    assert len(_reauth_flows(hass, entry)) == 1


async def test_real_refresh_outage_after_expiry_no_reauth(
    hass, mock_pettracer_client_init, mock_device, pettracer_error
):
    """An outage during re-login fails the update without starting reauth."""
    entry = _entry(hass)
    mock_pettracer_client_init.get_all_devices.return_value = [mock_device]
    await _setup(hass, entry, mock_pettracer_client_init)
    coordinator = hass.data[DOMAIN][entry.entry_id]

    mock_pettracer_client_init.get_all_devices.side_effect = pettracer_error(403)
    mock_pettracer_client_init.login.side_effect = pettracer_error()
    await coordinator.async_refresh()
    await hass.async_block_till_done()

    assert coordinator.last_update_success is False
    assert entry.state is ConfigEntryState.LOADED
    assert _reauth_flows(hass, entry) == []


async def test_real_setup_login_timeout_retries(hass, mock_pettracer_client_init):
    """A login timeout at setup (not wrapped by the library) is SETUP_RETRY."""
    entry = _entry(hass)
    mock_pettracer_client_init.login.side_effect = TimeoutError()

    await _setup(hass, entry, mock_pettracer_client_init)

    assert entry.state is ConfigEntryState.SETUP_RETRY
    assert _reauth_flows(hass, entry) == []
