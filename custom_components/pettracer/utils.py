"""Utility functions for the PetTracer integration."""

from __future__ import annotations


def battery_mv_to_percentage(mv: int) -> int:
    """Convert battery millivolts to percentage.

    Based on actual PetTracer device behavior:
    4200mV = 100%, 3600mV = 0%
    """
    if mv >= 4200:
        return 100
    if mv <= 3600:
        return 0
    return int(((mv - 3600) / 600) * 100)
