from django_logs_analyzer.filter_request import RequestLog
from django_logs_analyzer.handlers_stats import collect_handlers_stats, HandlerStats


def test_collect_handlers_stats():
    requests = [
        RequestLog(level="INFO", handler="/api/v1/reviews/"),
        RequestLog(level="INFO", handler="/admin/dashboard/"),
        RequestLog(level="DEBUG", handler="/api/v1/reviews/"),
        RequestLog(level="WARNING", handler="/admin/dashboard/"),
        RequestLog(level="ERROR", handler="/api/v1/reviews/"),
        RequestLog(level="CRITICAL", handler="/admin/dashboard/"),
        RequestLog(level="INFO", handler="/admin/dashboard/"),
    ]

    expected_stats = [
        HandlerStats(handler="/admin/dashboard/", debug=0, info=2, warning=1, error=0, critical=1),
        HandlerStats(handler="/api/v1/reviews/", debug=1, info=1, warning=0, error=1, critical=0),
    ]

    actual_stats = collect_handlers_stats(requests)
    assert actual_stats == expected_stats
    assert actual_stats[0].total == 4
    assert actual_stats[1].total == 3
