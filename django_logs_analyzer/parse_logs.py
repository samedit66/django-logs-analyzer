import datetime
from dataclasses import dataclass
import re
from typing import Iterable
from itertools import chain
from multiprocessing import Pool


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


def parse_logs_files(files: list[str]) -> Iterable[DjangoLog]:
    """Parses multiple log files into DjangoLog objects.
    Tries to do it in parallel.

    Args:
        files (list[str]): A list of file paths to log files.

    Returns:
        Iterable[DjangoLog]: An iterable of DjangoLog objects.
    """
    with Pool() as pool:
        # Тут, возможно, как-то по другому следует организовать чтение файлов,
        # чтобы гарантировано освобождать ресурсы, но для простоты пока так.
        logs = pool.map(
            _parse_logs_wrapper,
            [open(file, "r", encoding="utf8").readlines() for file in files],
        )
        return chain.from_iterable(logs)


def _parse_logs_wrapper(lines: Iterable[str]) -> list[DjangoLog]:
    """Wrapper function for parsing logs. Used for multiprocessing."""
    return list(parse_logs(lines))
