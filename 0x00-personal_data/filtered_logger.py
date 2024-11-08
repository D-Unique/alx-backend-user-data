#!/usr/bin/env python3
"""Module"""
import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """ this function that returns the log message obfuscated:"""
    for field in fields:
        reg = rf"({field})=[^{separator}]+"
        message = re.sub(reg,  rf"\1={redaction}", message)
    return message
