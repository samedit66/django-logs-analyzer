import datetime
from dataclasses import dataclass
import re
from typing import Iterable


@dataclass(frozen=True, slots=True)
class DjangoLog:
    time: datetime.datetime
    level: str
    source: str


@dataclass(frozen=True, slots=True)
class RequestLog(DjangoLog):
    request: str
    handler: str
    status_code: int


LOG_PATTERN = re.compile(
    r"^(?P<time>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3})\s+(?P<level>[A-Z]+)\s+django\.(?P<source>[^:]+):\s+(?P<rest>[^\n]+)$"
)


def parse_logs(lines: Iterable[str]) -> Iterable[tuple[DjangoLog, str]]:
    for line in lines:
        match = LOG_PATTERN.match(line)
        if match:
            time_str, level, source, rest = match.groups()
            time = datetime.datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S,%f")
            log = DjangoLog(time=time, level=level, source=source)
            yield log, rest


if __name__ == "__main__":
    log_lines = [
        "2025-03-28 12:44:46,000 INFO django.request: GET /api/v1/reviews/ 204 OK [192.168.1.59]",
        "2025-03-28 12:21:51,000 INFO django.request: GET /admin/dashboard/ 200 OK [192.168.1.68]",
        "2025-03-28 12:40:47,000 CRITICAL django.core.management: DatabaseError: Deadlock detected",
    ]

    for log, rest in parse_logs(log_lines):
        print(log, rest)
        