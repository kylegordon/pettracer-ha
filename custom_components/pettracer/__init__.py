"""The PetTracer integration."""

from __future__ import annotations

import logging
from datetime import timedelta

from pettracer import PetTracerClient, PetTracerError

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME, Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed, ConfigEntryNotReady
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, UPDATE_INTERVAL_SECONDS
from .utils import is_auth_error

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [
    Platform.BINARY_SENSOR,
    Platform.DEVICE_TRACKER,
    Platform.SENSOR,
]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up PetTracer from a config entry."""
    username = entry.data[CONF_USERNAME]
    password = entry.data[CONF_PASSWORD]

    # Create the PetTracer client
    client = PetTracerClient()

    # Authenticate
    try:
        await client.login(username, password)
    except PetTracerError as err:
        if is_auth_error(err):
            raise ConfigEntryAuthFailed("PetTracer rejected the credentials") from err
        raise ConfigEntryNotReady(f"Cannot connect to PetTracer: {err}") from err
    except TimeoutError as err:
        raise ConfigEntryNotReady("Timed out connecting to PetTracer") from err
    except Exception as err:
        _LOGGER.error("Unexpected error during PetTracer authentication: %s", err)
        raise ConfigEntryNotReady from err

    # Create update coordinator
    coordinator = PetTracerDataUpdateCoordinator(hass, client, entry)
    await coordinator.async_config_entry_first_refresh()

    # Store coordinator
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    # Forward the setup to platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


class PetTracerDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching PetTracer data."""

    def __init__(
        self, hass: HomeAssistant, client: PetTracerClient, entry: ConfigEntry
    ) -> None:
        """Initialize."""
        self.client = client
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=UPDATE_INTERVAL_SECONDS),
            config_entry=entry,
        )

    async def _async_update_data(self) -> dict:
        """Fetch data from PetTracer API, logging in again if the token expired."""
        try:
            devices = await self.client.get_all_devices()
        except PetTracerError as err:
            if not is_auth_error(err):
                raise UpdateFailed(
                    f"Error communicating with PetTracer API: {err}"
                ) from err
            _LOGGER.debug("PetTracer token rejected, logging in again")
            await self._async_relogin()
            try:
                devices = await self.client.get_all_devices()
            except PetTracerError as retry_err:
                if is_auth_error(retry_err):
                    raise ConfigEntryAuthFailed(
                        "PetTracer rejected the token straight after login"
                    ) from retry_err
                raise UpdateFailed(
                    f"Error communicating with PetTracer API: {retry_err}"
                ) from retry_err
        return {"devices": devices}

    async def _async_relogin(self) -> None:
        """Log in again with the stored credentials."""
        try:
            await self.client.login(
                self.config_entry.data[CONF_USERNAME],
                self.config_entry.data[CONF_PASSWORD],
            )
        except PetTracerError as err:
            if is_auth_error(err):
                raise ConfigEntryAuthFailed(
                    "PetTracer rejected the credentials"
                ) from err
            raise UpdateFailed(f"Error logging in to PetTracer: {err}") from err
