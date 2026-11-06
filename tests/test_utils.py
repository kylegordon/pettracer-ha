"""Tests for PetTracer utility functions."""

import pytest
from pettracer import PetTracerError

from custom_components.pettracer.utils import battery_mv_to_percentage, is_auth_error


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


@pytest.mark.parametrize("status", [401, 403])
def test_is_auth_error_true_for_rejected_credentials(pettracer_error, status):
    """401 (bad password) and 403 (bad token) are auth errors."""
    assert is_auth_error(pettracer_error(status)) is True


@pytest.mark.parametrize("status", [None, 404, 500, 503])
def test_is_auth_error_false_for_other_failures(pettracer_error, status):
    """Network errors and other HTTP statuses are not auth errors."""
    assert is_auth_error(pettracer_error(status)) is False


def test_is_auth_error_false_without_cause():
    """Library errors with no HTTP cause (bad JSON, missing token) are not auth errors."""
    assert is_auth_error(PetTracerError("Invalid JSON response")) is False
