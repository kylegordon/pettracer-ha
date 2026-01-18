"""Support for PetTracer device tracking."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.device_tracker import SourceType
from homeassistant.components.device_tracker.config_entry import TrackerEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up PetTracer device trackers based on a config entry."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]

    # Create a tracker for each device
    entities = []
    for device in coordinator.data.get("devices", []):
        entities.append(PetTracerDeviceTracker(coordinator, device))

    async_add_entities(entities, True)


class PetTracerDeviceTracker(CoordinatorEntity, TrackerEntity):
    """Representation of a PetTracer device tracker."""

    def __init__(self, coordinator, device):
        """Initialize the tracker."""
        super().__init__(coordinator)
        self._device = device
        self._device_id = device.id
        self._attr_unique_id = f"pettracer_{device.id}"
        self._attr_name = (
            device.details.name if device.details else f"PetTracer {device.id}"
        )

    def _get_device_data(self):
        """Get updated device data from coordinator."""
        devices = self.coordinator.data.get("devices", [])
        _LOGGER.debug(
            "Looking for device %s among %s devices in coordinator data",
            self._device_id,
            len(devices),
        )
        for device in devices:
            _LOGGER.debug(
                "Checking device ID %s against target %s", device.id, self._device_id
            )
            if device.id == self._device_id:
                _LOGGER.debug("Found matching device %s", self._device_id)
                return device
        _LOGGER.warning(
            "Device %s (tracker: %s) not found in coordinator data!",
            self._device_id,
            self._attr_name,
        )
        return None

    @property
    def device_info(self) -> dict[str, Any]:
        """Return device information about this tracker."""
        return {
            "identifiers": {(DOMAIN, self._device.id)},
            "name": self._attr_name,
            "manufacturer": "PetTracer",
            "model": "GPS Collar",
            "sw_version": self._device.sw if self._device.sw else None,
        }

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        device = self._get_device_data()
        is_available = device is not None
        _LOGGER.debug(
            "Device tracker %s (ID: %s) availability check: %s (device found: %s, has lastPos: %s)",
            self._attr_name,
            self._device_id,
            is_available,
            device is not None,
            device.lastPos is not None if device else False,
        )
        return is_available

    @property
    def source_type(self) -> SourceType:
        """Return the source type, eg gps or router, of the device."""
        return SourceType.GPS

    @property
    def latitude(self) -> float | None:
        """Return latitude value of the device."""
        device = self._get_device_data()
        if device and device.lastPos:
            lat = device.lastPos.posLat
            _LOGGER.debug(
                "Device tracker %s latitude: %s (has lastPos: %s, posLat: %s)",
                self._attr_name,
                lat,
                device.lastPos is not None,
                lat,
            )
            return lat
        _LOGGER.debug(
            "Device tracker %s latitude: None (device: %s, has lastPos: %s)",
            self._attr_name,
            device is not None,
            device.lastPos is not None if device else False,
        )
        return None

    @property
    def longitude(self) -> float | None:
        """Return longitude value of the device."""
        device = self._get_device_data()
        if device and device.lastPos:
            lon = device.lastPos.posLong
            _LOGGER.debug(
                "Device tracker %s longitude: %s (has lastPos: %s, posLong: %s)",
                self._attr_name,
                lon,
                device.lastPos is not None,
                lon,
            )
            return lon
        _LOGGER.debug(
            "Device tracker %s longitude: None (device: %s, has lastPos: %s)",
            self._attr_name,
            device is not None,
            device.lastPos is not None if device else False,
        )
        return None

    @property
    def location_accuracy(self) -> int:
        """Return the location accuracy of the device in meters."""
        device = self._get_device_data()
        if device and device.lastPos and device.lastPos.acc:
            return device.lastPos.acc
        return 0

    @property
    def battery_level(self) -> int | None:
        """Return the battery level of the device."""
        device = self._get_device_data()
        if device and device.bat:
            # Convert from millivolts to percentage (rough estimate)
            # Typical LiPo: 4.2V full, 3.0V empty
            # 4200mV = 100%, 3000mV = 0%
            mv = device.bat
            if mv >= 4200:
                return 100
            elif mv <= 3000:
                return 0
            else:
                return int(((mv - 3000) / 1200) * 100)
        return None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional state attributes."""
        attributes = {}
        device = self._get_device_data()
        
        if device:
            if device.bat:
                attributes["battery_voltage_mv"] = device.bat
            if device.lastContact:
                attributes["last_contact"] = device.lastContact
            if device.lastPos:
                if device.lastPos.sat:
                    attributes["satellites"] = device.lastPos.sat
                if device.lastPos.rssi:
                    attributes["signal_strength"] = device.lastPos.rssi
                if device.lastPos.timeMeasure:
                    attributes["position_time"] = device.lastPos.timeMeasure
            if device.status is not None:
                attributes["status"] = device.status
            if device.mode is not None:
                attributes["mode"] = device.mode
            if device.home is not None:
                attributes["at_home"] = device.home

        return attributes
