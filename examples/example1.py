from zlogger_kit import ZLog, ZLogConfig
from examples.modules import Module

config = ZLogConfig(
    module=Module.AUTH.value,
    json_format=False,
    log_path="logs/auth",
)
logger = ZLog.init(config)

logger.info("Starting authentication process", client_ip="192.168.1.100")
logger.info("Login successful", user_id="user_123")
logger.error(
    "Login failed",
    username="suspicious_user",
    ip="10.0.0.5",
    reason="Invalid credentials",
)
logger.warn(
    "Failed login attempt",
    username="suspicious_user",
    ip="10.0.0.5",
    reason="Invalid credentials",
)
logger.debug("Debug message", user_id="user_123")
logger.warn(
    "Failed login attempt",
    username="suspicious_user",
    ip="10.0.0.5",
    reason="Invalid credentials",
)
