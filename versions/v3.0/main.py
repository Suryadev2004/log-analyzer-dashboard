from core.parser import parse_log_file
from core.analytics import (
    calculate_total_requests,
    get_top_ips,
    get_status_code_distribution,
    get_top_endpoints,
    get_requests_per_minute
)

from detectors.brute_force import detect_brute_force
from detectors.spike_detector import detect_404_spike
from detectors.rate_detector import detect_high_request_rate


def main():
    file_path = "sample_logs/sample.log"
    logs = parse_log_file(file_path)

    print("=" * 40)
    print(" LOG ANALYSIS SUMMARY")
    print("=" * 40)

    print(f"\nTotal Requests: {calculate_total_requests(logs)}\n")

    print("Top IP Addresses:")
    for ip, count in get_top_ips(logs):
        print(f"{ip} → {count} requests")

    print("\nStatus Code Distribution:")
    for status, count in get_status_code_distribution(logs).items():
        print(f"{status} → {count}")

    print("\nTop Endpoints:")
    for endpoint, count in get_top_endpoints(logs):
        print(f"{endpoint} → {count}")

    print("\nRequests Per Minute:")
    rpm = get_requests_per_minute(logs)
    for minute, count in rpm.items():
        print(f"{minute} → {count} requests")

    # ===========================
    # 🚨 SECURITY ALERTS SECTION
    # ===========================

    print("\n" + "=" * 40)
    print(" SECURITY ALERTS")
    print("=" * 40)

    brute_force_alerts = detect_brute_force(logs)
    recon_alerts = detect_404_spike(logs)
    rate_alerts = detect_high_request_rate(logs)

    if not brute_force_alerts and not recon_alerts and not rate_alerts:
        print("No security threats detected.")

    # Brute Force Alerts
    for alert in brute_force_alerts:
        print(
            f"[ALERT] {alert['type']} from {alert['ip']} "
            f"({alert['failed_attempts']} failed attempts)"
        )

    # 404 Recon Alerts
    for alert in recon_alerts:
        print(
            f"[ALERT] {alert['type']} from {alert['ip']} "
            f"({alert['404_count']} 404 errors)"
        )

    # High Request Rate Alerts
    for alert in rate_alerts:
        print(
            f"[ALERT] {alert['type']} from {alert['ip']} "
            f"at {alert['minute']} "
            f"({alert['request_count']} requests in one minute)"
        )


if __name__ == "__main__":
    main()