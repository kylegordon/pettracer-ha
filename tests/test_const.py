"""Test constants for PetTracer integration."""
import json
from pathlib import Path

import pytest

from homeassistant.const import CONF_PASSWORD, CONF_USERNAME

from custom_components.pettracer.const import (
    DOMAIN,
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
    CHARGE_STATES,
    FLAG_ON_CHARGER,
)


def test_domain():
    """Test domain constant."""
    assert DOMAIN == "pettracer"


def test_conf_constants():
    """Test configuration constants match homeassistant.const values."""
    assert CONF_USERNAME == "username"
    assert CONF_PASSWORD == "password"


def test_update_interval():
    """Test update interval constant."""
    assert UPDATE_INTERVAL_SECONDS == 60
    assert isinstance(UPDATE_INTERVAL_SECONDS, int)
    assert UPDATE_INTERVAL_SECONDS > 0


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


def test_charge_state_constants():
    """Test charge state constants match the API's on-charger flags bit."""
    assert FLAG_ON_CHARGER == 0x02
    assert CHARGE_STATES == ["charging", "charged", "off_charger"]


COMPONENT_DIR = Path(__file__).parent.parent / "custom_components" / "pettracer"


def test_translations_in_sync():
    """Test translations/en.json matches strings.json."""
    strings = json.loads((COMPONENT_DIR / "strings.json").read_text())
    english = json.loads((COMPONENT_DIR / "translations" / "en.json").read_text())
    assert strings == english


def test_charge_state_translations_cover_states():
    """Test every charge state has a translation and no translation is orphaned."""
    strings = json.loads((COMPONENT_DIR / "strings.json").read_text())
    states = strings["entity"]["sensor"]["charge_state"]["state"]
    assert set(states) == set(CHARGE_STATES)
