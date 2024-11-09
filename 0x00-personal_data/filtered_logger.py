#!/usr/bin/env python3
"""Module"""
import logging
import re
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """ this function that returns the log message obfuscated:"""
    for field in fields:
        reg = rf"({field})=[^{separator}]+"
        message = re.sub(reg,  rf"\1={redaction}", message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """init"""
        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """format"""
        message = super().format(record)
        message = filter_datum(fields=self.fields,
                               redaction=RedactingFormatter.REDACTION,
                               message=message,
                               separator=RedactingFormatter.SEPARATOR)
        return message
