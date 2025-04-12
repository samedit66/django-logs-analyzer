from typing import Iterable

from django_logs_analyzer.parse_logs import parse_logs_files
from django_logs_analyzer.filter_request import filter_requests, RequestLog
from django_logs_analyzer.handlers_stats import collect_handlers_stats
from django_logs_analyzer.handlers_stats import HandlerStats


def handlers_report(files: Iterable[str]) -> str:
    """Generates a report of handler statistics from log files.

    Args:
        files (Iterable[str]): An iterable of file paths to log files.

    Returns:
        str: A formatted string representing the handler statistics report.
    """
    return _handlers_statistics_table(
        collect_handlers_stats(
            filter_requests(parse_logs_files(files)),
        )
    )


def _handlers_statistics_table(handlers_stats: Iterable[HandlerStats]) -> str:
    """Generates a statistics table from the collected handler statistics.

    Args:
        handlers_stats (Iterable[HandlerStats]): An iterable of HandlerStats objects containing statistics.

    Returns:
        str: A formatted string representing the statistics table.
    """
    lines = []

    requests_count = sum(hs.total for hs in handlers_stats)
    lines.append(f"Total requests: {requests_count}\n")

    lines.append(
        f"{'HANDLER':<30} {'DEBUG':<10} {'INFO':<10} {'WARNING':<10} {'ERROR':<10} {'CRITICAL':<10}"
    )

    for handler_stats in handlers_stats:
        lines.append(
            f"{handler_stats.handler:<30} "
            f"{handler_stats.debug:<10} "
            f"{handler_stats.info:<10} "
            f"{handler_stats.warning:<10} "
            f"{handler_stats.error:<10} "
            f"{handler_stats.critical:<10}"
        )

    return "\n".join(lines)
