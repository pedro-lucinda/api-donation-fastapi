import time

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.infra.logger.config import logger


class LoggerMiddleware(BaseHTTPMiddleware):
    """
    A middleware that logs the details of each request and response,
    including the method, path, status code, and the time taken to process
    the request.
    """

    async def dispatch(self, request: Request, call_next):
        """
        Override the default dispatch method to add logging.

        Args:
            request: The incoming HTTP request.
            call_next: A function that accepts the request and returns the
            response.

        Returns:
            The processed Response object.
        """
        # Get the start time
        start = time.time()
        # Process request before sending it to the endpoint
        response = await call_next(request)
        # log
        self.log_request(request, response, start)
        # Process response before returning it to the client
        return response

    def log_request(self, request: Request, response: Response, start: float):
        """
        Logs the request and response details along with the processing time.

        Args:
            request: The incoming HTTP request.
            response: The outgoing HTTP response.
            start: The start time of the request processing.
        """
        process_time = time.time() - start
        log_dict = {
            "process_time": process_time,
            "method": request.method,
            "path": request.url.path,
            "status": response.status_code,
        }
        logger.info(log_dict, extra=log_dict)
