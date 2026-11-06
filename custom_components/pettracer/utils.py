"""Utility functions for the PetTracer integration."""

from __future__ import annotations

from aiohttp import ClientResponseError
from pettracer import PetTracerError

# The PetTracer API answers a wrong password with 401 and an expired or
# invalid token with 403. pettracer-client wraps both (and every network
# error) in a plain PetTracerError, keeping the aiohttp error as __cause__.
AUTH_ERROR_STATUSES = frozenset({401, 403})


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


def is_auth_error(err: PetTracerError) -> bool:
    """Return True if a PetTracerError came from rejected credentials or token."""
    cause = err.__cause__
    return (
        isinstance(cause, ClientResponseError) and cause.status in AUTH_ERROR_STATUSES
    )
