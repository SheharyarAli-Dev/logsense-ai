import re

def parse_log_file(file_path):
    parsed_logs = []

    log_pattern = re.compile(
        r'(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s+'
        r'(?P<level>INFO|WARNING|ERROR|CRITICAL)\s+'
        r'(?P<message>.*)'
    )

    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        for line in file:
            match = log_pattern.match(line.strip())
            if match:
                parsed_logs.append(match.groupdict())

    return parsed_logs
