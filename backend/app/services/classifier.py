# Smarter keyword weights
ISSUE_KEYWORDS = {
    "Memory Issue": {
        "memory": 3,
        "ram": 2,
        "heap": 2,
        "leak": 4,
        "overflow": 4
    },
    "Crash Issue": {
        "crash": 4,
        "failed": 3,
        "fatal": 5,
        "shutdown": 3,
        "terminated": 4
    },
    "Disk Issue": {
        "disk": 3,
        "storage": 2,
        "space": 2,
        "full": 4,
        "write error": 3
    },
    "Network Issue": {
        "timeout": 3,
        "connection": 2,
        "unreachable": 4,
        "refused": 3,
        "network": 2
    }
}

def classify_log_message(message: str):
    message_lower = message.lower()
    scores = {}

    # Score each issue type
    for issue, keywords in ISSUE_KEYWORDS.items():
        score = 0
        for word, weight in keywords.items():
            if word in message_lower:
                score += weight
        if score > 0:
            scores[issue] = score

    # Choose highest score
    if scores:
        return max(scores, key=scores.get)
    else:
        return "Normal"
