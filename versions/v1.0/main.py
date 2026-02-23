from core.parser import parse_log_file
from core.analytics import (
    calculate_total_requests,
    get_top_ips,
    get_status_code_distribution,
    get_top_endpoints
)


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


if __name__ == "__main__":
    main()