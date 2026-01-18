"""Support for PetTracer sensors."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    PERCENTAGE,
    UnitOfElectricPotential,
    UnitOfLength,
    SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util.dt import parse_datetime
from datetime import datetime

from .const import (
    DOMAIN,
    MODE_LIVE,
    MODE_FAST_PLUS,
    MODE_FAST,
    MODE_NORMAL_PLUS,
    MODE_NORMAL,
    MODE_SLOW_PLUS,
    MODE_SLOW,
    VALID_MODES,
    MODE_NAMES,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up PetTracer sensors based on a config entry."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]

    # Create sensors for each device
    entities = []
    for device in coordinator.data.get("devices", []):
        # Battery level sensor
        entities.append(PetTracerBatterySensor(coordinator, device))

        # Battery voltage sensor
        entities.append(PetTracerBatteryVoltageSensor(coordinator, device))

        # Latitude sensor
        entities.append(PetTracerLatitudeSensor(coordinator, device))

        # Longitude sensor
        entities.append(PetTracerLongitudeSensor(coordinator, device))

        # GPS accuracy sensor
        entities.append(PetTracerGPSAccuracySensor(coordinator, device))

        # Last contact sensor
        entities.append(PetTracerLastContactSensor(coordinator, device))

        # Satellites sensor
        entities.append(PetTracerSatellitesSensor(coordinator, device))

        # Signal strength sensor
        entities.append(PetTracerSignalStrengthSensor(coordinator, device))

        # Position time sensor
        entities.append(PetTracerPositionTimeSensor(coordinator, device))

        # Status sensor
        entities.append(PetTracerStatusSensor(coordinator, device))

        # Mode sensor
        entities.append(PetTracerModeSensor(coordinator, device))

        # At home sensor
        entities.append(PetTracerAtHomeSensor(coordinator, device))

    async_add_entities(entities, True)


class PetTracerSensorBase(CoordinatorEntity, SensorEntity):
    """Base class for PetTracer sensors."""

    def __init__(self, coordinator, device):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._device = device
        self._device_id = device.id
        self._device_name = (
            device.details.name if device.details else f"PetTracer {device.id}"
        )

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


class PetTracerBatterySensor(PetTracerSensorBase):
    """Representation of a PetTracer battery level sensor."""

    def __init__(self, coordinator, device):
        """Initialize the sensor."""
        super().__init__(coordinator, device)
        self._attr_unique_id = f"pettracer_{device.id}_battery_level"
        self._attr_name = f"{self._device_name} Battery Level"
        self._attr_device_class = SensorDeviceClass.BATTERY
        self._attr_native_unit_of_measurement = PERCENTAGE
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_icon = "mdi:battery"

    @property
    def native_value(self) -> int | None:
        """Return the state of the sensor."""
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


class PetTracerBatteryVoltageSensor(PetTracerSensorBase):
    """Representation of a PetTracer battery voltage sensor."""

    def __init__(self, coordinator, device):
        """Initialize the sensor."""
        super().__init__(coordinator, device)
        self._attr_unique_id = f"pettracer_{device.id}_battery_voltage"
        self._attr_name = f"{self._device_name} Battery Voltage"
        self._attr_device_class = SensorDeviceClass.VOLTAGE
        self._attr_native_unit_of_measurement = UnitOfElectricPotential.MILLIVOLT
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_icon = "mdi:flash"

    @property
    def native_value(self) -> int | None:
        """Return the state of the sensor."""
        device = self._get_device_data()
        if device and device.bat:
            return device.bat
        return None


class PetTracerLatitudeSensor(PetTracerSensorBase):
    """Representation of a PetTracer latitude sensor."""

    def __init__(self, coordinator, device):
        """Initialize the sensor."""
        super().__init__(coordinator, device)
        self._attr_unique_id = f"pettracer_{device.id}_latitude"
        self._attr_name = f"{self._device_name} Latitude"
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_icon = "mdi:crosshairs-gps"

    @property
    def native_value(self) -> float | None:
        """Return the state of the sensor."""
        device = self._get_device_data()
        if device and device.lastPos:
            return device.lastPos.posLat
        return None


class PetTracerLongitudeSensor(PetTracerSensorBase):
    """Representation of a PetTracer longitude sensor."""

    def __init__(self, coordinator, device):
        """Initialize the sensor."""
        super().__init__(coordinator, device)
        self._attr_unique_id = f"pettracer_{device.id}_longitude"
        self._attr_name = f"{self._device_name} Longitude"
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_icon = "mdi:crosshairs-gps"

    @property
    def native_value(self) -> float | None:
        """Return the state of the sensor."""
        device = self._get_device_data()
        if device and device.lastPos:
            return device.lastPos.posLong
        return None


class PetTracerGPSAccuracySensor(PetTracerSensorBase):
    """Representation of a PetTracer GPS accuracy sensor."""

    def __init__(self, coordinator, device):
        """Initialize the sensor."""
        super().__init__(coordinator, device)
        self._attr_unique_id = f"pettracer_{device.id}_gps_accuracy"
        self._attr_name = f"{self._device_name} GPS Accuracy"
        self._attr_device_class = SensorDeviceClass.DISTANCE
        self._attr_native_unit_of_measurement = UnitOfLength.METERS
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_icon = "mdi:map-marker-radius"

    @property
    def native_value(self) -> int | None:
        """Return the state of the sensor."""
        device = self._get_device_data()
        if device and device.lastPos and device.lastPos.acc is not None:
            return device.lastPos.acc
        return None


class PetTracerLastContactSensor(PetTracerSensorBase):
    """Representation of a PetTracer last contact sensor."""

    def __init__(self, coordinator, device):
        """Initialize the sensor."""
        super().__init__(coordinator, device)
        self._attr_unique_id = f"pettracer_{device.id}_last_contact"
        self._attr_name = f"{self._device_name} Last Contact"
        self._attr_device_class = SensorDeviceClass.TIMESTAMP
        self._attr_icon = "mdi:clock-outline"

    @property
    def native_value(self) -> datetime | None:
        """Return the state of the sensor."""
        device = self._get_device_data()
        if device and device.lastContact:
            return device.lastContact
        return None


class PetTracerSatellitesSensor(PetTracerSensorBase):
    """Representation of a PetTracer satellites sensor."""

    def __init__(self, coordinator, device):
        """Initialize the sensor."""
        super().__init__(coordinator, device)
        self._attr_unique_id = f"pettracer_{device.id}_satellites"
        self._attr_name = f"{self._device_name} Satellites"
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_icon = "mdi:satellite-variant"

    @property
    def native_value(self) -> int | None:
        """Return the state of the sensor."""
        device = self._get_device_data()
        if device and device.lastPos and device.lastPos.sat is not None:
            return device.lastPos.sat
        return None


class PetTracerSignalStrengthSensor(PetTracerSensorBase):
    """Representation of a PetTracer signal strength sensor."""

    def __init__(self, coordinator, device):
        """Initialize the sensor."""
        super().__init__(coordinator, device)
        self._attr_unique_id = f"pettracer_{device.id}_signal_strength"
        self._attr_name = f"{self._device_name} Signal Strength"
        self._attr_device_class = SensorDeviceClass.SIGNAL_STRENGTH
        self._attr_native_unit_of_measurement = SIGNAL_STRENGTH_DECIBELS_MILLIWATT
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_icon = "mdi:signal"

    @property
    def native_value(self) -> int | None:
        """Return the state of the sensor."""
        device = self._get_device_data()
        if device and device.lastPos and device.lastPos.rssi is not None:
            return device.lastPos.rssi
        return None


class PetTracerPositionTimeSensor(PetTracerSensorBase):
    """Representation of a PetTracer position time sensor."""

    def __init__(self, coordinator, device):
        """Initialize the sensor."""
        super().__init__(coordinator, device)
        self._attr_unique_id = f"pettracer_{device.id}_position_time"
        self._attr_name = f"{self._device_name} Position Time"
        self._attr_device_class = SensorDeviceClass.TIMESTAMP
        self._attr_icon = "mdi:map-clock"

    @property
    def native_value(self) -> datetime | None:
        """Return the state of the sensor."""
        device = self._get_device_data()
        if device and device.lastPos and device.lastPos.timeMeasure:
            # Try to parse the time string and return as datetime object
            try:
                dt = parse_datetime(device.lastPos.timeMeasure)
                if dt:
                    return dt
            except (ValueError, TypeError):
                pass
            # Return as-is if parsing fails
            return device.lastPos.timeMeasure
        return None


class PetTracerStatusSensor(PetTracerSensorBase):
    """Representation of a PetTracer status sensor."""

    def __init__(self, coordinator, device):
        """Initialize the sensor."""
        super().__init__(coordinator, device)
        self._attr_unique_id = f"pettracer_{device.id}_status"
        self._attr_name = f"{self._device_name} Status"
        self._attr_icon = "mdi:information-outline"

    @property
    def native_value(self) -> int | None:
        """Return the state of the sensor."""
        device = self._get_device_data()
        if device and device.status is not None:
            return device.status
        return None


class PetTracerModeSensor(PetTracerSensorBase):
    """Representation of a PetTracer mode sensor."""

    def __init__(self, coordinator, device):
        """Initialize the sensor."""
        super().__init__(coordinator, device)
        self._attr_unique_id = f"pettracer_{device.id}_mode"
        self._attr_name = f"{self._device_name} Mode"
        self._attr_icon = "mdi:cog-outline"

    @property
    def native_value(self) -> int | None:
        """Return the state of the sensor."""
        device = self._get_device_data()
        if device and device.mode is not None:
            # Log warning if mode is not in expected values
            if device.mode not in VALID_MODES:
                _LOGGER.warning(
                    "Unknown mode value %s for device %s. Expected one of: %s",
                    device.mode,
                    self._device_id,
                    VALID_MODES,
                )
            return device.mode
        return None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional attributes."""
        device = self._get_device_data()
        if device and device.mode is not None:
            mode_name = MODE_NAMES.get(device.mode, f"Unknown ({device.mode})")
            return {"mode_name": mode_name}
        return {}


class PetTracerAtHomeSensor(PetTracerSensorBase):
    """Representation of a PetTracer at home sensor."""

    def __init__(self, coordinator, device):
        """Initialize the sensor."""
        super().__init__(coordinator, device)
        self._attr_unique_id = f"pettracer_{device.id}_at_home"
        self._attr_name = f"{self._device_name} At Home"
        self._attr_icon = "mdi:home"

    @property
    def native_value(self) -> str | None:
        """Return the state of the sensor."""
        device = self._get_device_data()
        if device and device.home is not None:
            return "true" if device.home else "false"
        return None
