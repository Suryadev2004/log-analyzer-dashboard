from collections import defaultdict


def detect_404_spike(logs, threshold=3):
    """
    Detect possible reconnaissance activity based on repeated 404 errors.
    """

    not_found_counts = defaultdict(int)

    for log in logs:
        if log["status_code"] == 404:
            not_found_counts[log["ip"]] += 1

    alerts = []

    for ip, count in not_found_counts.items():
        if count >= threshold:
            alerts.append({
                "type": "Possible Reconnaissance (404 Spike)",
                "ip": ip,
                "404_count": count
            })

    return alerts