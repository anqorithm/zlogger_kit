"""ZLoggerKit - A structured logging utility for Python applications."""

from importlib.metadata import PackageNotFoundError, version

from zlogger_kit.zlog import ZLog
from zlogger_kit.models import ZLogConfig, ZNetworkRequest, ZNetworkResponse
from zlogger_kit.middleware import ZLogMiddleware

try:
    __version__ = version("zlogger-kit")
except PackageNotFoundError:  # running from a source checkout without install
    __version__ = "0.0.0"

__all__ = [
    "ZLog",
    "ZLogConfig",
    "ZNetworkRequest",
    "ZNetworkResponse",
    "ZLogMiddleware",
]
