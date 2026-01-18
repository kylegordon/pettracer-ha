"""Constants for the PetTracer integration."""

DOMAIN = "pettracer"
CONF_USERNAME = "username"
CONF_PASSWORD = "password"

# Update intervals
UPDATE_INTERVAL_SECONDS = 60  # Poll every 60 seconds for location updates

# Device tracker platform
PLATFORM_DEVICE_TRACKER = "device_tracker"

# Mode mappings - PetTracer device modes
# Maps device mode values to their standardized numeric representation
MODE_LIVE = 11      # Live mode
MODE_FAST_PLUS = 8  # Fast+ mode
MODE_FAST = 1       # Fast mode
MODE_NORMAL_PLUS = 14  # Normal+ mode
MODE_NORMAL = 2     # Normal mode
MODE_SLOW_PLUS = 7  # Slow+ mode
MODE_SLOW = 3       # Slow mode

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
