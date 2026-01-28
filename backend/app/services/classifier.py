def classify_log(log):
    message = log["message"].lower()

    if "memory" in message or "ram" in message:
        return "Memory Issue"

    elif "disk" in message or "storage" in message:
        return "Storage Issue"

    elif "network" in message or "timeout" in message or "connection" in message:
        return "Network Issue"

    elif "permission" in message or "access denied" in message:
        return "Permission Issue"

    elif "crash" in message or "fatal" in message or "shutdown" in message:
        return "Crash Issue"

    elif log["level"] == "ERROR" or log["level"] == "CRITICAL":
        return "General Error"

    else:
        return "Normal"
