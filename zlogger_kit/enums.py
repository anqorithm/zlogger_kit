"""Enums module containing network operation and log level enumerations."""

from enum import Enum


class ZNetworkOperation(str, Enum):
    """Enumeration for different types of network operations.

    This enum inherits from str to allow for string-like behavior while
    maintaining enum functionality.
    """

    REQUEST = "request"
    """Represents an outgoing network request operation."""

    RESPONSE = "response"
    """Represents an incoming network response operation."""


class ZLogLevel(str, Enum):
    """Enumeration for different logging levels with associated priorities.

    This enum inherits from str and includes a priority value for each level,
    allowing for both string representation and priority-based sorting/filtering.
    """

    DEBUG = ("DEBUG", "P10")
    """Debug level logging with lowest priority (P10)."""

    INFO = ("INFO", "P20")
    """Informational level logging with low-medium priority (P20)."""

    WARNING = ("WARNING", "P30")
    """Warning level logging with medium-high priority (P30)."""

    ERROR = ("ERROR", "P40")
    """Error level logging with highest priority (P40)."""

    def __new__(cls, value, priority):
        """Create a new ZLogLevel enum instance with a value and priority.

        Args:
            value (str): The string value of the log level.
            priority (str): The priority level string (e.g., 'P10', 'P20').

        Returns:
            ZLogLevel: A new enum instance with the specified value and priority.
        """
        obj = str.__new__(cls, value)
        obj._value_ = value
        obj.priority = priority
        return obj
