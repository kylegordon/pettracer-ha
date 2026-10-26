"""Fixtures for PetTracer tests."""
from unittest.mock import AsyncMock, create_autospec, patch

import pytest
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from pettracer import PetTracerClient
from pettracer.types import Device

# This fixture enables loading custom integrations in pytest tests
pytest_plugins = "pytest_homeassistant_custom_component"


@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations):
    """Enable custom integrations for all tests."""
    yield


@pytest.fixture
def mock_setup_entry() -> AsyncMock:
    """Mock setting up a config entry."""
    with patch(
        "custom_components.pettracer.async_setup_entry", return_value=True
    ) as mock_setup:
        yield mock_setup


def _device_payload(**overrides):
    """Return a device record shaped like the PetTracer getccs API response."""
    payload = {
        "id": 12345,
        "accuWarn": 3810,
        "safetyZone": False,
        "hw": 656643,
        "sw": 656393,
        "bl": 656386,
        "bat": 4100,
        "chg": 1,
        "userId": 15979,
        "masterHs": {
            "id": 10775,
            "posLat": 51.5074,
            "posLong": -0.1278,
            "hw": 656384,
            "sw": 656388,
            "bl": 656385,
            "bat": 0,
            "userId": None,
            "status": 0,
            "lastContact": "2026-01-11T10:30:00.000+0000",
            "devMode": False,
        },
        "mode": 1,
        "modeSet": 1,
        "status": 0,
        "search": False,
        "lastTlgNr": -42,
        "lastContact": "2026-01-11T10:30:00.000+0000",
        "lastPos": {
            "id": 110294833,
            "posLat": 51.5074,
            "posLong": -0.1278,
            "fixS": 3,
            "fixP": 2,
            "horiPrec": 12,
            "sat": 8,
            "rssi": -65,
            "acc": 10,
            "flags": 32,
            "timeMeasure": "2026-01-11T10:30:00.000+0000",
            "timeDb": "2026-01-11T10:30:05.000+0000",
        },
        "devMode": False,
        "details": {
            "id": 12345,
            "image": None,
            "img": "img1570960283064022523",
            "color": 255,
            "birth": "2018-07-15T23:00:00.000+0000",
            "name": "Fluffy",
        },
        "led": False,
        "ble": False,
        "buz": False,
        "lastRssi": -30,
        "flags": 2,
        "searchModeDuration": -1,
        "masterStatus": "ACTIVE",
        "home": True,
        "homeSince": "2026-01-11T09:00:00.000+0000",
        "owner": True,
        "fiFo": [],
    }
    payload.update(overrides)
    return payload


@pytest.fixture
def device_payload():
    """Return the payload builder, for tests that need a variant device."""
    return _device_payload


def _mock_client_instance():
    """Return a PetTracerClient mock that rejects methods the library lacks."""
    return create_autospec(PetTracerClient, instance=True)


@pytest.fixture
def mock_pettracer_client_init():
    """Mock PetTracerClient for __init__.py."""
    with patch("custom_components.pettracer.PetTracerClient") as mock_client:
        client_instance = _mock_client_instance()
        mock_client.return_value = client_instance
        yield client_instance


@pytest.fixture
def mock_device():
    """Create a PetTracer device using the library's own parser."""
    return Device.from_dict(_device_payload())


@pytest.fixture
def mock_device_no_position():
    """Create a PetTracer device without position data."""
    return Device.from_dict(
        _device_payload(
            id=12346,
            bat=3800,
            chg=0,
            home=False,
            lastContact="2026-01-11T10:00:00.000+0000",
            lastPos=None,
            details={"id": 12346, "name": "Rex"},
        )
    )


@pytest.fixture
def config_entry_data():
    """Return mock config entry data."""
    return {
        CONF_USERNAME: "test@example.com",
        CONF_PASSWORD: "test_password",
    }
