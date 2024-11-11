#!/usr/bin/env python3
"""this is a module"""
import bcrypt


def hash_password(password: str) -> bcrypt.hashpw:
    """this func returns a hashed password"""
    byte = password.encode('utf-8')
    return bcrypt.hashpw(byte, bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    passwordbyte = password.encode('utf-8')
    result = bcrypt.checkpw(passwordbyte, hashed_password)
    return result
