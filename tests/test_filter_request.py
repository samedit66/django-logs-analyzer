from datetime import datetime

from django_logs_analyzer.parse_logs import DjangoLog
from django_logs_analyzer.filter_request import filter_requests, RequestLog


def test_filter_requests():
    logs = [
        DjangoLog(
            time=datetime(2025, 3, 28, 12, 44, 46, 0),
            level="INFO",
            source="request",
            message="GET /api/v1/reviews/ 204 OK [192.168.1.59]",
        ),
        DjangoLog(
            time=datetime(2025, 3, 28, 12, 21, 51, 0),
            level="INFO",
            source="request",
            message="GET /admin/dashboard/ 200 OK [192.168.1.68]",
        ),
        DjangoLog(
            time=datetime(2025, 3, 28, 12, 40, 47, 0),
            level="CRITICAL",
            source="core.management",
            message="DatabaseError: Deadlock detected",
        ),
    ]

    expected_requests = [
        RequestLog(level="INFO", handler="/api/v1/reviews/"),
        RequestLog(level="INFO", handler="/admin/dashboard/"),
    ]

    filtered_requests = list(filter_requests(logs))
    assert filtered_requests == expected_requests
