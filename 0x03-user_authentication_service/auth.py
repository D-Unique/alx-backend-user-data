#!/usr/bin/env python3
""" This module contains the Auth class"""
from bcrypt import hashpw, gensalt, checkpw
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from user import User


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a new user with the provided email and password
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))

    def valid_login(self, email: str, password: str) -> bool:
        """Check if the provided email and password are valid
        """
        try:
            user = self._db.find_user_by(email=email)
            bpassword = password.encode('utf-8')
            hash_password = user.hashed_password
            return checkpw(password=bpassword, hashed_password=hash_password)
        except NoResultFound:
            return False


def _hash_password(password: str) -> bytes:
    """Hashes a password
    """
    return hashpw(password.encode('utf-8'), gensalt())
