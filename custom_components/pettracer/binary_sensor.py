"""Support for PetTracer binary sensors."""

from __future__ import annotations

from typing import Any

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up PetTracer binary sensors based on a config entry."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]

    entities: list = []
    for device in coordinator.data.get("devices", []):
        entities.append(PetTracerAtHomeBinarySensor(coordinator, device))
        entities.append(PetTracerChargingBinarySensor(coordinator, device))

    async_add_entities(entities, True)


class PetTracerAtHomeBinarySensor(CoordinatorEntity, BinarySensorEntity):
    """Representation of a PetTracer at home binary sensor."""

    _attr_device_class = BinarySensorDeviceClass.PRESENCE

    def __init__(self, coordinator, device):
        """Initialize the binary sensor."""
        super().__init__(coordinator)
        self._device = device
        self._device_id = device.id
        self._device_name = (
            device.details.name if device.details else f"PetTracer {device.id}"
        )
        self._attr_unique_id = f"pettracer_{device.id}_at_home"
        self._attr_name = f"{self._device_name} At Home"

    @property
    def device_info(self) -> dict[str, Any]:
        """Return device information about this sensor."""
        return {
            "identifiers": {(DOMAIN, self._device_id)},
            "name": self._device_name,
            "manufacturer": "PetTracer",
            "model": "GPS Collar",
            "sw_version": self._device.sw if self._device.sw else None,
        }

    def _get_device_data(self):
        """Get updated device data from coordinator."""
        for device in self.coordinator.data.get("devices", []):
            if device.id == self._device_id:
                return device
        return None

    @property
    def is_on(self) -> bool | None:
        """Return true if the pet is at home."""
        device = self._get_device_data()
        if device and device.home is not None:
            return device.home
        return None


class PetTracerChargingBinarySensor(CoordinatorEntity, BinarySensorEntity):
    """Representation of a PetTracer charging binary sensor."""

    _attr_device_class = BinarySensorDeviceClass.BATTERY_CHARGING

    def __init__(self, coordinator, device):
        """Initialize the binary sensor."""
        super().__init__(coordinator)
        self._device = device
        self._device_id = device.id
        self._device_name = (
            device.details.name if device.details else f"PetTracer {device.id}"
        )
        self._attr_unique_id = f"pettracer_{device.id}_charging"
        self._attr_name = f"{self._device_name} Charging"

    @property
    def device_info(self) -> dict[str, Any]:
        """Return device information about this sensor."""
        return {
            "identifiers": {(DOMAIN, self._device_id)},
            "name": self._device_name,
            "manufacturer": "PetTracer",
            "model": "GPS Collar",
            "sw_version": self._device.sw if self._device.sw else None,
        }

    def _get_device_data(self):
        """Get updated device data from coordinator."""
        for device in self.coordinator.data.get("devices", []):
            if device.id == self._device_id:
                return device
        return None

    @property
    def is_on(self) -> bool | None:
        """Return true if the collar is charging."""
        device = self._get_device_data()
        if device and device.chg is not None:
            return bool(device.chg)
        return None
