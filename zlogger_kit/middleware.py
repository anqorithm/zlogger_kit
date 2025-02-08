"""Middleware module for network request/response logging.

This module provides middleware functionality to automatically log network
requests and responses using the ZLog logger.
"""

from typing import Any, Callable
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from zlogger_kit.models import ZNetworkRequest, ZNetworkResponse
from zlogger_kit.zlog import ZLog


class ZLogMiddleware(BaseHTTPMiddleware):
    """ASGI middleware for logging network requests and responses.

    This middleware automatically logs all incoming HTTP requests and their
    corresponding responses using the provided ZLog logger instance.

    Args:
        app: The ASGI application.
        logger: ZLog instance used for logging requests and responses.
    """

    def __init__(self, app: Any, logger: ZLog):
        """Initialize the middleware with an app and logger instance."""
        super().__init__(app)
        self.logger = logger

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process and log the request/response cycle.

        Args:
            request: The incoming HTTP request.
            call_next: Callable that processes the request through the app.

        Returns:
            The response from the application.
        """
        network_request = ZNetworkRequest(
            method=request.method,
            url=str(request.url),
            headers=dict(request.headers),
            body=await request.body() if hasattr(request, "body") else None,
        )
        self.logger.network_request(
            network_request,
            ip=request.client.host if hasattr(request, "client") else None,
        )

        response = await call_next(request)

        network_response = ZNetworkResponse(
            status_code=response.status_code,
            headers=dict(response.headers),
            body=getattr(response, "body", None),
        )
        self.logger.network_response(
            network_response,
            ip=request.client.host if hasattr(request, "client") else None,
        )

        return response
