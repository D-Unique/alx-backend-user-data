#!/usr/bin/env python3
"""Module"""
import logging
import re
from typing import List, Tuple
import mysql.connector as mc
import os


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class"""
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


def get_db() -> mc.connection.MySQLConnection:
    """this function helps connect to the database"""
    username = os.getenv('PERSONAL_DATA_DB_USERNAME', "root")
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD', "")
    database = os.getenv('PERSONAL_DATA_DB_NAME')
    host = os.getenv('PERSONAL_DATA_DB_HOST', "localhost")
    cnx = mc.connect(
        user=username,
        password=password,
        host=host,
        database=database,
    )
    return cnx


PII_FIELDS: Tuple = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """ this function that returns the log message obfuscated:"""
    for field in fields:
        reg = rf"({field})=[^{separator}]+"
        message = re.sub(reg,  rf"\1={redaction}", message)
    return message


def get_logger() -> logging.Logger:
    """this function creates a custom logger"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    formatter = logging.Formatter(RedactingFormatter(PII_FIELDS))
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    return logger


def main() -> None:
    logger = get_logger()
    try:
        with get_db() as connection:
            with connection.cursor as cursor:
                quary = ('SELECT * FROM users')
                cursor.execute(quary)
                rows = cursor.fetchall()
                redacteddata = filter_datum(PII_FIELDS, "***", rows, ';')
                logger.info(redacteddata)
    except Exception as e:
        logger.error(f"an error {e} occured")


if __name__ == "__main__":
    main()
