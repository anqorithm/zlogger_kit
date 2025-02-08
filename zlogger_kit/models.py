from pydantic import BaseModel


class ZLogConfig(BaseModel):
    """Configuration model for ZLogger.

    Attributes:
        module: Name of the module being logged
        time_zone: Timezone for log timestamps (default: "Asia/Riyadh")
        json_format: Whether to output logs in JSON format (default: True)
        log_path: Directory path for log files (default: "logs")
    """

    module: str
    time_zone: str = "Asia/Riyadh"
    json_format: bool = True
    log_path: str = "logs"


class ZNetworkRequest(BaseModel):
    """Model representing an HTTP network request.

    Attributes:
        method: HTTP method (GET, POST, etc.)
        url: Target URL for the request
        headers: Optional dictionary of HTTP headers
        body: Optional request body content
    """

    method: str
    url: str
    headers: dict | None = None
    body: object | None = None


class ZNetworkResponse(BaseModel):
    """Model representing an HTTP network response.

    Attributes:
        status_code: HTTP status code of the response
        headers: Optional dictionary of response headers
        body: Optional response body content
    """

    status_code: int
    headers: dict | None = None
    body: object | None = None
