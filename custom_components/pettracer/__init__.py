"""The PetTracer integration."""
from __future__ import annotations

import logging
from datetime import timedelta

from pettracer import PetTracerClient, PetTracerError

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed, ConfigEntryNotReady
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import CONF_PASSWORD, CONF_USERNAME, DOMAIN, UPDATE_INTERVAL_SECONDS

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.DEVICE_TRACKER]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up PetTracer from a config entry."""
    username = entry.data[CONF_USERNAME]
    password = entry.data[CONF_PASSWORD]

    # Create the PetTracer client
    client = PetTracerClient()

    # Authenticate
    try:
        await hass.async_add_executor_job(client.login, username, password)
    except PetTracerError as err:
        _LOGGER.error("Failed to authenticate with PetTracer: %s", err)
        raise ConfigEntryAuthFailed from err
    except Exception as err:
        _LOGGER.error("Unexpected error during PetTracer authentication: %s", err)
        raise ConfigEntryNotReady from err

    # Create update coordinator
    coordinator = PetTracerDataUpdateCoordinator(hass, client)
    await coordinator.async_config_entry_first_refresh()

    # Store coordinator
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    # Forward the setup to the device_tracker platform
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


class PetTracerDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching PetTracer data."""

    def __init__(self, hass: HomeAssistant, client: PetTracerClient) -> None:
        """Initialize."""
        self.client = client
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=UPDATE_INTERVAL_SECONDS),
        )

    async def _async_update_data(self):
        """Fetch data from PetTracer API."""
        try:
            # Fetch all devices
            devices = await self.hass.async_add_executor_job(
                self.client.get_all_devices
            )
            return {"devices": devices}
        except PetTracerError as err:
            raise UpdateFailed(f"Error communicating with PetTracer API: {err}") from err
