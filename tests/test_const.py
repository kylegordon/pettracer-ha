"""Test constants for PetTracer integration."""
import pytest

from custom_components.pettracer.const import (
    CONF_PASSWORD,
    CONF_USERNAME,
    DOMAIN,
    PLATFORM_DEVICE_TRACKER,
    UPDATE_INTERVAL_SECONDS,
)


def test_domain():
    """Test domain constant."""
    assert DOMAIN == "pettracer"


def test_conf_constants():
    """Test configuration constants."""
    assert CONF_USERNAME == "username"
    assert CONF_PASSWORD == "password"


def test_update_interval():
    """Test update interval constant."""
    assert UPDATE_INTERVAL_SECONDS == 60
    assert isinstance(UPDATE_INTERVAL_SECONDS, int)
    assert UPDATE_INTERVAL_SECONDS > 0


def test_platform_constant():
    """Test platform constant."""
    assert PLATFORM_DEVICE_TRACKER == "device_tracker"
