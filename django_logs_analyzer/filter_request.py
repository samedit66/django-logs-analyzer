from dataclasses import dataclass
from typing import Iterable

from django_logs_analyzer.parse_logs import DjangoLog


@dataclass(frozen=True, slots=True)
class RequestLog:
    level: str
    handler: str


def filter_requests(logs: Iterable[DjangoLog]) -> Iterable[RequestLog]:
    """Filters log entries to extract request logs.

    Args:
        logs (Iterable[DjangoLog]): An iterable of DjangoLog objects.

    Returns:
        Iterable[RequestLog]: An iterable of RequestLog objects.
    """
    for log in logs:
        if log.source == "request":
            # We assume that the handler starts with "/".
            handler = None
            for part in log.message.split():
                if part.startswith("/"):
                    handler = part
                    break

            # Not sure, if this can ever happen, but just in case.
            if handler is None:
                continue

            yield RequestLog(level=log.level, handler=handler)
