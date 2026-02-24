from collections import defaultdict


def detect_high_request_rate(logs, threshold=4):
    """
    Detect high request rate from a single IP within the same minute.
    """

    rate_tracker = defaultdict(int)

    for log in logs:
        minute = log["timestamp"].replace(second=0, microsecond=0)
        key = (log["ip"], minute)
        rate_tracker[key] += 1

    alerts = []

    for (ip, minute), count in rate_tracker.items():
        if count >= threshold:
            alerts.append({
                "type": "High Request Rate",
                "ip": ip,
                "minute": minute,
                "request_count": count
            })

    return alerts