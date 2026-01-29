from collections import Counter

def analyze_root_cause(logs):
    categories = [log["category"] for log in logs if log["category"] != "Normal"]

    if not categories:
        return {
            "root_cause": "No major issues detected",
            "severity": "Low"
        }

    count = Counter(categories)
    main_issue = count.most_common(1)[0][0]

    critical_logs = [log for log in logs if log["level"] == "CRITICAL"]
    error_logs = [log for log in logs if log["level"] == "ERROR"]

    if critical_logs:
        severity = "High"
    elif error_logs:
        severity = "Medium"
    else:
        severity = "Low"

    return {
        "root_cause": main_issue,
        "severity": severity,
        "issue_count": dict(count)
    }
