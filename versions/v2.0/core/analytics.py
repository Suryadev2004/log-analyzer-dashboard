from collections import Counter, defaultdict


def calculate_total_requests(logs):
    return len(logs)


def get_top_ips(logs, top_n=5):
    ip_counts = Counter(log["ip"] for log in logs)
    return ip_counts.most_common(top_n)


def get_status_code_distribution(logs):
    status_counts = Counter(log["status_code"] for log in logs)
    return dict(status_counts)


def get_top_endpoints(logs, top_n=5):
    endpoint_counts = Counter(log["endpoint"] for log in logs)
    return endpoint_counts.most_common(top_n)


def get_requests_per_minute(logs):
    requests_per_minute = defaultdict(int)

    for log in logs:
        # Round timestamp to minute
        minute = log["timestamp"].replace(second=0, microsecond=0)
        requests_per_minute[minute] += 1

    # Sort by time
    return dict(sorted(requests_per_minute.items()))