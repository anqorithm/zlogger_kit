import os
import json
from datetime import datetime
from zoneinfo import ZoneInfo
import structlog
from zlogger_kit.models import ZLogConfig, ZNetworkRequest, ZNetworkResponse
from zlogger_kit.enums import ZLogLevel, ZNetworkOperation


class ZLog:
    """A logging utility class that provides structured logging capabilities.

    This class implements a singleton pattern per module and handles both JSON and
    text-based logging with configurable timezone support.

    Attributes:
        _instances (dict): Class-level dictionary storing singleton instances per module.
    """

    _instances = {}

    def __init__(self, config: ZLogConfig):
        """Initialize a new ZLog instance.

        Args:
            config (ZLogConfig): Configuration object containing logging settings.
        """
        self._config = config
        os.makedirs(self._config.log_path, exist_ok=True)
        self._logger = self._create_logger()
        self._current_time = None

    @property
    def config(self) -> ZLogConfig:
        """Get the current logging configuration.

        Returns:
            ZLogConfig: The current configuration object.
        """
        return self._config

    @classmethod
    def init(cls, config: ZLogConfig) -> "ZLog":
        """Initialize or retrieve a ZLog instance for a specific module.

        This method implements the singleton pattern per module.

        Args:
            config (ZLogConfig): Configuration object containing logging settings.

        Returns:
            ZLog: A new or existing ZLog instance for the specified module.
        """
        if config.module not in cls._instances:
            cls._instances[config.module] = cls(config)
        return cls._instances[config.module]

    def _create_logger(self) -> object:
        """Create and configure a structlog logger instance.

        Returns:
            object: Configured structlog logger instance.
        """
        structlog.configure(
            processors=[
                structlog.processors.TimeStamper(fmt="iso"),
                structlog.processors.JSONRenderer(),
            ],
            context_class=dict,
            logger_factory=structlog.PrintLoggerFactory(),
            wrapper_class=structlog.BoundLogger,
            cache_logger_on_first_use=True,
        )
        return structlog.get_logger(module=self._config.module)

    def set_current_time(self, time: datetime) -> None:
        """Set a custom current time for logging.

        Args:
            time (datetime): Custom datetime to use for logging timestamps.
        """
        self._current_time = time

    def _get_current_time(self) -> datetime:
        """Get the current time for logging.

        Returns:
            datetime: Current time with configured timezone or custom time if set.
        """
        if self._current_time is not None:
            return self._current_time
        return datetime.now(ZoneInfo(self._config.time_zone))

    def _get_log_file_path(self) -> str:
        """Generate the log file path based on current date and module name.

        Returns:
            str: Full path to the log file.
        """
        current_date = self._get_current_time().strftime("%Y-%m-%d")
        return os.path.join(
            self._config.log_path, f"{self._config.module.lower()}-{current_date}.log"
        )

    def _write_log(self, message: str, **kwargs) -> None:
        """Write a log entry to the configured log file.

        Args:
            message (str): The log message to write.
            **kwargs: Additional fields to include in the log entry.
        """
        log_file = self._get_log_file_path()

        level = kwargs.get("level", "")
        priority = ""
        try:
            level_enum = ZLogLevel(level)
            priority = level_enum.priority
            level_prefix = f"[{level}]:[{priority}]"
        except ValueError:
            level_prefix = ""

        log_entry = {
            "timestamp": self._get_current_time().isoformat(),
            "module": self._config.module,
            "priority": priority,
            "message": message,
            **kwargs,
        }

        log_content = (
            json.dumps(log_entry) + "\n"
            if self._config.json_format
            else f"{level_prefix} [{log_entry['timestamp']}] {message} {json.dumps(kwargs) if kwargs else ''}\n"
        )

        with open(log_file, "a", encoding="utf-8") as f:
            f.write(log_content)

    def debug(self, message: str, error: Exception = None, **kwargs) -> None:
        """Write a debug level log message.

        Args:
            message (str): The log message.
            error (Exception, optional): Exception to log. Defaults to None.
            **kwargs: Additional fields to include in the log entry.
        """
        if error:
            kwargs["error"] = str(error)
        self._write_log(message, level=ZLogLevel.DEBUG.value, **kwargs)

    def log(self, message: str, error: Exception = None, **kwargs) -> None:
        """Write an info level log message (alias for info).

        Args:
            message (str): The log message.
            error (Exception, optional): Exception to log. Defaults to None.
            **kwargs: Additional fields to include in the log entry.
        """
        if error:
            kwargs["error"] = str(error)
        self._write_log(message, level=ZLogLevel.INFO.value, **kwargs)

    def info(self, message: str, error: Exception = None, **kwargs) -> None:
        """Write an info level log message.

        Args:
            message (str): The log message.
            error (Exception, optional): Exception to log. Defaults to None.
            **kwargs: Additional fields to include in the log entry.
        """
        if error:
            kwargs["error"] = str(error)
        self._write_log(message, level=ZLogLevel.INFO.value, **kwargs)

    def warn(self, message: str, error: Exception = None, **kwargs) -> None:
        """Write a warning level log message.

        Args:
            message (str): The log message.
            error (Exception, optional): Exception to log. Defaults to None.
            **kwargs: Additional fields to include in the log entry.
        """
        if error:
            kwargs["error"] = str(error)
        self._write_log(message, level=ZLogLevel.WARNING.value, **kwargs)

    def error(self, message: str, error: Exception = None, **kwargs) -> None:
        """Write an error level log message.

        Args:
            message (str): The log message.
            error (Exception, optional): Exception to log. Defaults to None.
            **kwargs: Additional fields to include in the log entry.
        """
        if error:
            kwargs["error"] = str(error)
        self._write_log(message, level=ZLogLevel.ERROR.value, **kwargs)

    def network_request(self, request: ZNetworkRequest, ip: str = None) -> None:
        """Log a network request.

        Args:
            request (ZNetworkRequest): The network request to log.
            ip (str, optional): IP address associated with the request. Defaults to None.
        """
        message = f"{request.method} {request.url}"
        self._write_log(
            message,
            level=ZLogLevel.INFO.value,
            operation=ZNetworkOperation.REQUEST.value,
            method=request.method,
            url=request.url,
            ip=ip,
        )

    def network_response(self, response: ZNetworkResponse, ip: str = None) -> None:
        """Log a network response.

        Args:
            response (ZNetworkResponse): The network response to log.
            ip (str, optional): IP address associated with the response. Defaults to None.
        """
        message = f"{response.status_code}"
        self._write_log(
            message,
            level=ZLogLevel.INFO.value,
            operation=ZNetworkOperation.RESPONSE.value,
            status_code=response.status_code,
            ip=ip,
        )
