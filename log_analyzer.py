import argparse
import json
import re
import sys
from collections import Counter

LOG_RE = re.compile(
    r'^(?P<ip>\S+) \S+ \S+ \[(?P<time>[^\]]+)\] '
    r'"(?P<method>[A-Z]+) (?P<url>\S+)[^"]*" '
    r'(?P<status>\d{3}) (?P<size>\d+|-)'
)


def parse_line(line):
    """Return a dict with the parsed fields, or None if the line is not valid."""
    match = LOG_RE.match(line.strip())
    if not match:
        return None
    data = match.groupdict()
    data["size"] = 0 if data["size"] == "-" else int(data["size"])
    data["hour"] = data["time"].split(":")[1]
    return data


def analyze(path, top=5):
    """Analyze the log file and return the report as a dictionary."""
    ips, urls, classes, error_hours = Counter(), Counter(), Counter(), Counter()
    total = bad_lines = total_bytes = 0

    with open(path, encoding="utf-8", errors="replace") as f:
        for line in f:
            if not line.strip():
                continue
            row = parse_line(line)
            if row is None:
                bad_lines += 1
                continue
            total += 1
            total_bytes += row["size"]
            ips[row["ip"]] += 1
            urls[row["url"]] += 1
            classes[row["status"][0] + "xx"] += 1
            if row["status"][0] in "45":
                error_hours[row["hour"]] += 1

    return {
        "total_requests": total,
        "invalid_lines": bad_lines,
        "total_megabytes": round(total_bytes / 1_000_000, 2),
        "status_classes": dict(sorted(classes.items())),
        "top_ips": ips.most_common(top),
        "top_urls": urls.most_common(top),
        "errors_by_hour": dict(sorted(error_hours.items())),
    }


def print_report(report):
    print(f"Total requests:   {report['total_requests']}")
    print(f"Invalid lines:    {report['invalid_lines']}")
    print(f"Data transferred: {report['total_megabytes']} MB")
    print("\nStatus classes:")
    for name, count in report["status_classes"].items():
        print(f"  {name}: {count}")
    print("\nTop IP addresses:")
    for ip, count in report["top_ips"]:
        print(f"  {ip:<18}{count}")
    print("\nTop URLs:")
    for url, count in report["top_urls"]:
        print(f"  {url:<22}{count}")
    print("\nErrors (4xx/5xx) by hour:")
    for hour, count in report["errors_by_hour"].items():
        print(f"  {hour}:00  {'#' * count} {count}")


def main():
    parser = argparse.ArgumentParser(description="Analyze a web server access log.")
    parser.add_argument("logfile", help="path to the access log")
    parser.add_argument("--top", type=int, default=5, help="how many top items to show (default 5)")
    parser.add_argument("--json", metavar="FILE", help="also save the report as JSON")
    args = parser.parse_args()

    try:
        report = analyze(args.logfile, args.top)
    except FileNotFoundError:
        sys.exit(f"File not found: {args.logfile}")

    print_report(report)
    if args.json:
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        print(f"\nReport saved to {args.json}")


if __name__ == "__main__":
    main()
