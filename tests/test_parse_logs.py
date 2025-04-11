from datetime import datetime

from django_logs_analyzer.parse_logs import parse_logs, DjangoLog


def test_parse_logs():
    log_lines = [
        "2025-03-28 12:44:46,000 INFO django.request: GET /api/v1/reviews/ 204 OK [192.168.1.59]",
        "2025-03-28 12:21:51,000 INFO django.request: GET /admin/dashboard/ 200 OK [192.168.1.68]",
        "2025-03-28 12:40:47,000 CRITICAL django.core.management: DatabaseError: Deadlock detected",
    ]

    expected_logs = [
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

    parsed_logs = list(parse_logs(log_lines))
    assert parsed_logs == expected_logs
