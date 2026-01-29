def suggest_solution(root_cause):
    solutions = {
        "Memory Issue": [
            "Check for memory leaks in application",
            "Increase system RAM",
            "Restart memory-intensive services"
        ],
        "Storage Issue": [
            "Clean up disk space",
            "Check log file sizes",
            "Expand storage volume"
        ],
        "Network Issue": [
            "Check server connectivity",
            "Verify firewall settings",
            "Inspect network latency"
        ],
        "Permission Issue": [
            "Check file permissions",
            "Verify user roles and access rights"
        ],
        "Crash Issue": [
            "Inspect application crash logs",
            "Restart the service",
            "Check recent code deployments"
        ],
        "General Error": [
            "Review error logs in detail",
            "Check configuration files"
        ]
    }

    return solutions.get(root_cause, ["No suggestion available"])
