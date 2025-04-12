from dataclasses import dataclass
from typing import Iterable

from django_logs_analyzer.filter_request import RequestLog


@dataclass(slots=True)
class HandlerStats:
    """Data class for storing statistics about log handlers."""

    handler: str
    debug: int = 0 
    info: int = 0
    warning: int = 0
    error: int = 0
    critical: int = 0

    @property
    def total(self) -> int:
        return self.debug + self.info + self.warning + self.error + self.critical


def collect_handlers_stats(request_logs: Iterable[RequestLog]) -> Iterable[HandlerStats]:
    """Collects statistics about log handlers from request logs."""
    handlers = {}

    for log in request_logs:
        if log.handler not in handlers:
            handlers[log.handler] = HandlerStats(handler=log.handler)

        match log.level:
            case "DEBUG":
                handlers[log.handler].debug += 1
            case "INFO":
                handlers[log.handler].info += 1
            case "WARNING":
                handlers[log.handler].warning += 1
            case "ERROR":
                handlers[log.handler].error += 1
            case "CRITICAL":
                handlers[log.handler].critical += 1

    return handlers.values()
