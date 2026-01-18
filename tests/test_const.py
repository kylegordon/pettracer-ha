"""Test constants for PetTracer integration."""
import pytest

from custom_components.pettracer.const import (
    CONF_PASSWORD,
    CONF_USERNAME,
    DOMAIN,
    PLATFORM_DEVICE_TRACKER,
    UPDATE_INTERVAL_SECONDS,
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


def test_mode_constants():
    """Test mode constants."""
    assert MODE_LIVE == 11
    assert MODE_FAST_PLUS == 8
    assert MODE_FAST == 1
    assert MODE_NORMAL_PLUS == 14
    assert MODE_NORMAL == 2
    assert MODE_SLOW_PLUS == 7
    assert MODE_SLOW == 3


def test_valid_modes():
    """Test valid modes set."""
    assert VALID_MODES == {1, 2, 3, 7, 8, 11, 14}
    assert len(VALID_MODES) == 7
    assert MODE_LIVE in VALID_MODES
    assert MODE_FAST_PLUS in VALID_MODES
    assert MODE_FAST in VALID_MODES
    assert MODE_NORMAL_PLUS in VALID_MODES
    assert MODE_NORMAL in VALID_MODES
    assert MODE_SLOW_PLUS in VALID_MODES
    assert MODE_SLOW in VALID_MODES


def test_mode_names():
    """Test mode names mapping."""
    assert MODE_NAMES[MODE_LIVE] == "Live"
    assert MODE_NAMES[MODE_FAST_PLUS] == "Fast+"
    assert MODE_NAMES[MODE_FAST] == "Fast"
    assert MODE_NAMES[MODE_NORMAL_PLUS] == "Normal+"
    assert MODE_NAMES[MODE_NORMAL] == "Normal"
    assert MODE_NAMES[MODE_SLOW_PLUS] == "Slow+"
    assert MODE_NAMES[MODE_SLOW] == "Slow"
    assert len(MODE_NAMES) == 7
