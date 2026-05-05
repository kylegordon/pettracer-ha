"""Tests for PetTracer utility functions."""

from custom_components.pettracer.utils import battery_mv_to_percentage


def test_battery_mv_to_percentage_full():
    """Test full battery."""
    assert battery_mv_to_percentage(4200) == 100


def test_battery_mv_to_percentage_empty():
    """Test empty battery."""
    assert battery_mv_to_percentage(3600) == 0


def test_battery_mv_to_percentage_over_max():
    """Test voltage above max."""
    assert battery_mv_to_percentage(4500) == 100


def test_battery_mv_to_percentage_under_min():
    """Test voltage below min."""
    assert battery_mv_to_percentage(3000) == 0


def test_battery_mv_to_percentage_mid():
    """Test mid-range voltage."""
    assert battery_mv_to_percentage(3900) == 50


def test_battery_mv_to_percentage_typical():
    """Test typical voltage values."""
    assert battery_mv_to_percentage(4100) == 83
    assert battery_mv_to_percentage(3800) == 33
    assert battery_mv_to_percentage(4000) == 66
