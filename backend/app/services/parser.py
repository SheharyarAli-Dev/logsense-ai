import re
from typing import Union
import io

def parse_log_file(file_input: Union[str, io.BytesIO]):
    """
    Parses a log file and returns a list of log dictionaries.
    
    Parameters:
        file_input: Either a file path (str) or a file-like object (BytesIO / TextIO)
    """
    parsed_logs = []

    log_pattern = re.compile(
        r'(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s+'
        r'(?P<level>INFO|WARNING|ERROR|CRITICAL)\s+'
        r'(?P<message>.*)'
    )

    # Check if input is a path or file-like
    if isinstance(file_input, str):
        file = open(file_input, 'r', encoding='utf-8', errors='ignore')
        close_after = True
    else:
        # If bytes, decode to string and wrap in TextIOWrapper
        if isinstance(file_input, io.BytesIO):
            file_input.seek(0)
            file_input = io.TextIOWrapper(file_input, encoding='utf-8', errors='ignore')
        file = file_input
        close_after = False

    for line in file:
        match = log_pattern.match(line.strip())
        if match:
            parsed_logs.append(match.groupdict())

    if close_after:
        file.close()

    return parsed_logs
