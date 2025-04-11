import datetime
from dataclasses import dataclass
import re
from typing import Iterable


@dataclass(frozen=True, slots=True)
class DjangoLog:
    """Data class for Django log entries."""
    time: datetime.datetime
    level: str
    source: str
    message: str


LOG_PATTERN = re.compile(
    r"^(?P<time>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3})\s+(?P<level>[A-Z]+)\s+django\.(?P<source>[^:]+):\s+(?P<message>[^\n]+)$"
)


def parse_logs(lines: Iterable[str]) -> Iterable[DjangoLog]:
    """Parses Django log lines into DjangoLog objects.

    Args:
        lines (Iterable[str]): An iterable of log lines.

    Returns:
        Iterable[DjangoLog]: An iterable of DjangoLog objects.
    """
    for line in lines:
        match = LOG_PATTERN.match(line)
        if match:
            time_str, level, source, message = match.groups()
            time = datetime.datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S,%f")
            yield DjangoLog(time=time, level=level, source=source, message=message)
            