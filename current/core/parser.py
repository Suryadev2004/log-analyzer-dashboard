import re


# Apache Common Log Format Regex
LOG_PATTERN = re.compile(
    r'(?P<ip>\S+) - - '
    r'\[(?P<timestamp>[^\]]+)\] '
    r'"(?P<method>\S+) (?P<endpoint>\S+) HTTP/\d\.\d" '
    r'(?P<status>\d{3}) \d+'
)


def parse_log_file(file_path):
    logs = []

    with open(file_path, "r") as file:
        for line in file:
            match = LOG_PATTERN.match(line)
            if match:
                log_entry = {
                    "ip": match.group("ip"),
                    "timestamp": match.group("timestamp"),
                    "method": match.group("method"),
                    "endpoint": match.group("endpoint"),
                    "status_code": int(match.group("status"))
                }
                logs.append(log_entry)

    return logs