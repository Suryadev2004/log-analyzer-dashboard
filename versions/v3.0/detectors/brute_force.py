from collections import defaultdict


def detect_brute_force(logs, threshold=3):
    failed_attempts = defaultdict(int)

    for log in logs:
        if log["status_code"] == 401 and "/login" in log["endpoint"]:
            failed_attempts[log["ip"]] += 1

    alerts = []

    for ip, count in failed_attempts.items():
        if count >= threshold:
            alerts.append({
                "type": "Brute Force Attempt",
                "ip": ip,
                "failed_attempts": count
            })

    return alerts