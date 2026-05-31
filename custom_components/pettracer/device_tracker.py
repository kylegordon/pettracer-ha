"""Support for PetTracer device tracking."""

from __future__ import annotations

from typing import Any

from homeassistant.components.device_tracker import SourceType
from homeassistant.components.device_tracker.config_entry import TrackerEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .utils import battery_mv_to_percentage


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up PetTracer device trackers based on a config entry."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]

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
        for device in self.coordinator.data.get("devices", []):
            if device.id == self._device_id:
                return device
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
        return self._get_device_data() is not None

    @property
    def source_type(self) -> SourceType:
        """Return the source type, eg gps or router, of the device."""
        return SourceType.GPS

    @property
    def latitude(self) -> float | None:
        """Return latitude value of the device."""
        device = self._get_device_data()
        if device and device.lastPos:
            return device.lastPos.posLat
        return None

    @property
    def longitude(self) -> float | None:
        """Return longitude value of the device."""
        device = self._get_device_data()
        if device and device.lastPos:
            return device.lastPos.posLong
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
            return battery_mv_to_percentage(device.bat)
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
