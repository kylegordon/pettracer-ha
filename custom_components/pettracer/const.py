"""Constants for the PetTracer integration."""

DOMAIN = "pettracer"

# Update intervals
UPDATE_INTERVAL_SECONDS = 60  # Poll every 60 seconds for location updates

# Mode mappings - PetTracer device modes
# Maps device mode values to their standardized numeric representation
MODE_LIVE = 11  # Live mode
MODE_FAST_PLUS = 8  # Fast+ mode
MODE_FAST = 1  # Fast mode
MODE_NORMAL_PLUS = 14  # Normal+ mode
MODE_NORMAL = 2  # Normal mode
MODE_SLOW_PLUS = 7  # Slow+ mode
MODE_SLOW = 3  # Slow mode

# Valid mode values
VALID_MODES = {
    MODE_LIVE,
    MODE_FAST_PLUS,
    MODE_FAST,
    MODE_NORMAL_PLUS,
    MODE_NORMAL,
    MODE_SLOW_PLUS,
    MODE_SLOW,
}

# Mode names mapping for display
MODE_NAMES = {
    MODE_LIVE: "Live",
    MODE_FAST_PLUS: "Fast+",
    MODE_FAST: "Fast",
    MODE_NORMAL_PLUS: "Normal+",
    MODE_NORMAL: "Normal",
    MODE_SLOW_PLUS: "Slow+",
    MODE_SLOW: "Slow",
}

# Charge state - derived from the collar's `chg` and `flags` API fields.
# `chg` is 1 while the collar is actively charging (fast charge). Bit 0x02 of
# `flags` is set while the collar sits on its charger, whether or not it is
# still charging. The PetTracer app and portal use the same two fields.
FLAG_ON_CHARGER = 0x02
CHARGE_STATE_CHARGING = "charging"
CHARGE_STATE_CHARGED = "charged"
CHARGE_STATE_OFF_CHARGER = "off_charger"
CHARGE_STATES = [
    CHARGE_STATE_CHARGING,
    CHARGE_STATE_CHARGED,
    CHARGE_STATE_OFF_CHARGER,
]
