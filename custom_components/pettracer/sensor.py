"""Support for PetTracer sensors."""

from __future__ import annotations

import logging
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    PERCENTAGE,
    SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
    EntityCategory,
    UnitOfElectricPotential,
    UnitOfLength,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util.dt import parse_datetime

from .const import (
    DOMAIN,
    MODE_NAMES,
    VALID_MODES,
)
from .utils import battery_mv_to_percentage

_LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True, kw_only=True)
class PetTracerSensorEntityDescription(SensorEntityDescription):
    """Describe a PetTracer sensor entity."""

    value_fn: Callable[[Any], Any]
    extra_attrs_fn: Callable[[Any], dict[str, Any]] | None = None
    display_name: str = ""


def _get_battery_level(device: Any) -> int | None:
    """Get battery level as percentage."""
    if device and device.bat:
        return battery_mv_to_percentage(device.bat)
    return None


def _get_battery_voltage(device: Any) -> int | None:
    """Get battery voltage in millivolts."""
    if device and device.bat:
        return device.bat
    return None


def _get_latitude(device: Any) -> float | None:
    """Get latitude."""
    if device and device.lastPos:
        return device.lastPos.posLat
    return None


def _get_longitude(device: Any) -> float | None:
    """Get longitude."""
    if device and device.lastPos:
        return device.lastPos.posLong
    return None


def _get_gps_accuracy(device: Any) -> int | None:
    """Get GPS accuracy."""
    if device and device.lastPos and device.lastPos.acc is not None:
        return device.lastPos.acc
    return None


def _get_last_contact(device: Any) -> datetime | None:
    """Get last contact time."""
    if device and device.lastContact:
        return device.lastContact
    return None


def _get_satellites(device: Any) -> int | None:
    """Get satellite count."""
    if device and device.lastPos and device.lastPos.sat is not None:
        return device.lastPos.sat
    return None


def _get_signal_strength(device: Any) -> int | None:
    """Get signal strength."""
    if device and device.lastPos and device.lastPos.rssi is not None:
        return device.lastPos.rssi
    return None


def _get_position_time(device: Any) -> datetime | None:
    """Get position time."""
    if device and device.lastPos and device.lastPos.timeMeasure:
        try:
            dt = parse_datetime(device.lastPos.timeMeasure)
            if dt:
                return dt
        except (ValueError, TypeError):
            pass
        return device.lastPos.timeMeasure
    return None


def _get_status(device: Any) -> int | None:
    """Get device status."""
    if device and device.status is not None:
        return device.status
    return None


def _get_mode(device: Any) -> str | None:
    """Get device mode name."""
    if device and device.mode is not None:
        mode_name = MODE_NAMES.get(device.mode, "Unrecognized")
        if device.mode not in VALID_MODES:
            _LOGGER.warning(
                "Unknown mode value %s for device %s. Expected one of: %s",
                device.mode,
                device.id,
                sorted(VALID_MODES),
            )
        return mode_name
    return None


def _get_mode_attrs(device: Any) -> dict[str, Any]:
    """Get mode extra attributes."""
    if device and device.mode is not None:
        return {"mode_number": device.mode}
    return {}


SENSOR_DESCRIPTIONS: tuple[PetTracerSensorEntityDescription, ...] = (
    PetTracerSensorEntityDescription(
        key="battery_level",
        display_name="Battery Level",
        device_class=SensorDeviceClass.BATTERY,
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=_get_battery_level,
    ),
    PetTracerSensorEntityDescription(
        key="battery_voltage",
        display_name="Battery Voltage",
        translation_key="battery_voltage",
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement=UnitOfElectricPotential.MILLIVOLT,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=_get_battery_voltage,
    ),
    PetTracerSensorEntityDescription(
        key="latitude",
        display_name="Latitude",
        translation_key="latitude",
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:crosshairs-gps",
        value_fn=_get_latitude,
    ),
    PetTracerSensorEntityDescription(
        key="longitude",
        display_name="Longitude",
        translation_key="longitude",
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:crosshairs-gps",
        value_fn=_get_longitude,
    ),
    PetTracerSensorEntityDescription(
        key="gps_accuracy",
        display_name="GPS Accuracy",
        translation_key="gps_accuracy",
        device_class=SensorDeviceClass.DISTANCE,
        native_unit_of_measurement=UnitOfLength.METERS,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        icon="mdi:map-marker-radius",
        value_fn=_get_gps_accuracy,
    ),
    PetTracerSensorEntityDescription(
        key="last_contact",
        display_name="Last Contact",
        translation_key="last_contact",
        device_class=SensorDeviceClass.TIMESTAMP,
        icon="mdi:clock-outline",
        value_fn=_get_last_contact,
    ),
    PetTracerSensorEntityDescription(
        key="satellites",
        display_name="Satellites",
        translation_key="satellites",
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        icon="mdi:satellite-variant",
        value_fn=_get_satellites,
    ),
    PetTracerSensorEntityDescription(
        key="signal_strength",
        display_name="Signal Strength",
        translation_key="signal_strength",
        device_class=SensorDeviceClass.SIGNAL_STRENGTH,
        native_unit_of_measurement=SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        icon="mdi:signal",
        value_fn=_get_signal_strength,
    ),
    PetTracerSensorEntityDescription(
        key="position_time",
        display_name="Position Time",
        translation_key="position_time",
        device_class=SensorDeviceClass.TIMESTAMP,
        icon="mdi:map-clock",
        value_fn=_get_position_time,
    ),
    PetTracerSensorEntityDescription(
        key="status",
        display_name="Status",
        translation_key="status",
        icon="mdi:information-outline",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=_get_status,
    ),
    PetTracerSensorEntityDescription(
        key="mode",
        display_name="Mode",
        translation_key="mode",
        icon="mdi:cog-outline",
        value_fn=_get_mode,
        extra_attrs_fn=_get_mode_attrs,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up PetTracer sensors based on a config entry."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]

    entities: list[PetTracerSensor] = []
    for device in coordinator.data.get("devices", []):
        entities.extend(
            PetTracerSensor(coordinator, device, description)
            for description in SENSOR_DESCRIPTIONS
        )

    async_add_entities(entities, True)


class PetTracerSensor(CoordinatorEntity, SensorEntity):
    """Representation of a PetTracer sensor."""

    entity_description: PetTracerSensorEntityDescription

    def __init__(self, coordinator, device, description: PetTracerSensorEntityDescription):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._device = device
        self._device_id = device.id
        self._device_name = (
            device.details.name if device.details else f"PetTracer {device.id}"
        )
        self._attr_unique_id = f"pettracer_{device.id}_{description.key}"
        self._attr_name = f"{self._device_name} {description.display_name}"

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
    def native_value(self):
        """Return the state of the sensor."""
        device = self._get_device_data()
        return self.entity_description.value_fn(device)

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional attributes."""
        if self.entity_description.extra_attrs_fn:
            device = self._get_device_data()
            return self.entity_description.extra_attrs_fn(device)
        return {}

