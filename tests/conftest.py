"""Fixtures for PetTracer tests."""
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime

import pytest

from homeassistant.const import CONF_PASSWORD, CONF_USERNAME

from custom_components.pettracer.const import DOMAIN


@pytest.fixture
def mock_setup_entry() -> AsyncMock:
    """Mock setting up a config entry."""
    with patch(
        "custom_components.pettracer.async_setup_entry", return_value=True
    ) as mock_setup:
        yield mock_setup


@pytest.fixture
def mock_pettracer_client():
    """Mock PetTracerClient."""
    with patch("custom_components.pettracer.config_flow.PetTracerClient") as mock_client:
        client_instance = MagicMock()
        client_instance.login = MagicMock()
        client_instance.is_authenticated = True
        client_instance.token = "test-token"
        client_instance.user_name = "Test User"
        mock_client.return_value = client_instance
        yield mock_client


@pytest.fixture
def mock_pettracer_client_init():
    """Mock PetTracerClient for __init__.py."""
    with patch("custom_components.pettracer.PetTracerClient") as mock_client:
        client_instance = MagicMock()
        client_instance.login = MagicMock()
        client_instance.is_authenticated = True
        client_instance.token = "test-token"
        client_instance.get_all_devices = MagicMock()
        mock_client.return_value = client_instance
        yield client_instance


@pytest.fixture
def mock_device():
    """Create a mock PetTracer device."""
    device = MagicMock()
    device.id = 12345
    device.bat = 4100
    device.status = 0
    device.mode = 1
    device.home = True
    device.sw = 656393
    device.lastContact = datetime(2026, 1, 11, 10, 30, 0)
    
    # Device details
    device.details = MagicMock()
    device.details.name = "Fluffy"
    
    # Last position
    device.lastPos = MagicMock()
    device.lastPos.posLat = 51.5074
    device.lastPos.posLong = -0.1278
    device.lastPos.acc = 10
    device.lastPos.sat = 8
    device.lastPos.rssi = -65
    device.lastPos.timeMeasure = "2026-01-11T10:30:00.000+0000"
    
    return device


@pytest.fixture
def mock_device_no_position():
    """Create a mock PetTracer device without position data."""
    device = MagicMock()
    device.id = 12346
    device.bat = 3800
    device.status = 0
    device.mode = 1
    device.home = False
    device.sw = 656393
    device.lastContact = datetime(2026, 1, 11, 10, 0, 0)
    
    # Device details
    device.details = MagicMock()
    device.details.name = "Rex"
    
    # No position
    device.lastPos = None
    
    return device


@pytest.fixture
def config_entry_data():
    """Return mock config entry data."""
    return {
        CONF_USERNAME: "test@example.com",
        CONF_PASSWORD: "test_password",
    }
