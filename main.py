from django_logs_analyzer.parse_logs import parse_logs


if __name__ == "__main__":
    log_lines = [
        "2025-03-28 12:44:46,000 INFO django.request: GET /api/v1/reviews/ 204 OK [192.168.1.59]",
        "2025-03-28 12:21:51,000 INFO django.request: GET /admin/dashboard/ 200 OK [192.168.1.68]",
        "2025-03-28 12:40:47,000 CRITICAL django.core.management: DatabaseError: Deadlock detected",
    ]

    for log in parse_logs(log_lines):
        print(log)
        