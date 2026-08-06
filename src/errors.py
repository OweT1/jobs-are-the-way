# Standard Library Packages

# Third Party Packages

# Local Project

# Case-insensitive signals that identify a rate-limit / quota-hitting error.
# The base client wraps provider exceptions into a generic Exception (losing
# the original type), so detection relies on the class name and message text.
_RATE_LIMIT_SIGNALS = (
    "x-rate-limit-exceeded",
    "rate_limit",
    "rate-limit",
    "rate limit",
    "ratelimit",
    "too many requests",
    "http 429",
    "429 too many requests",
)


def is_rate_limit_error(error: Exception) -> bool:
    """Returns True if `error` indicates a rate-limit / quota condition."""
    class_name = type(error).__name__.lower()
    message = str(error).lower()
    return class_name == "ratelimiterror" or any(s in message for s in _RATE_LIMIT_SIGNALS)
