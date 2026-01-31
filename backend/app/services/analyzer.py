from collections import Counter
from datetime import datetime, timedelta
from collections import defaultdict
def determine_root_cause(issue_count):
    if not issue_count:
        return "No Major Issue"

    importance = {
        "Crash Issue": 3,
        "Memory Issue": 2,
        "Disk Issue": 2,
        "Network Issue": 2,
        "General Error": 1
    }

    weighted_scores = {}
    for issue, count in issue_count.items():
        weight = importance.get(issue, 1)
        weighted_scores[issue] = count * weight

    return max(weighted_scores, key=weighted_scores.get)


def calculate_severity(issue_count):
    total_issues = sum(issue_count.values())

    if issue_count.get("Crash Issue", 0) > 0:
        return "Critical"

    if issue_count.get("Memory Issue", 0) >= 2:
        return "High"

    if total_issues >= 3:
        return "Medium"

    return "Low"

def analyze_root_cause(logs):
    categories = [log["category"] for log in logs if log["category"] != "Normal"]

    if not categories:
        return {
            "root_cause": "No major issues detected",
            "severity": "Low",
            "issue_count": {}
        }

    # Count issue occurrences
    count = Counter(categories)
    issue_count = dict(count)

    # 🧠 USE SMART AI LOGIC HERE
    root_cause = determine_root_cause(issue_count)
    severity = calculate_severity(issue_count)

    return {
        "root_cause": root_cause,
        "severity": severity,
        "issue_count": issue_count
    }

def analyze_trends(logs, interval_minutes=10):
    """
    Analyze trends of issues over time.
    Returns counts of each category per time interval.
    """
    # Prepare timeline buckets
    timeline = defaultdict(lambda: defaultdict(int))

    for log in logs:
        ts = datetime.strptime(log["timestamp"], "%Y-%m-%d %H:%M:%S")
        # Round timestamp to nearest interval
        bucket = ts - timedelta(
            minutes=ts.minute % interval_minutes,
            seconds=ts.second,
            microseconds=ts.microsecond
        )
        timeline[bucket][log["category"]] += 1

    # Convert defaultdict to normal dict for JSON response
    return {str(k): dict(v) for k, v in timeline.items()}