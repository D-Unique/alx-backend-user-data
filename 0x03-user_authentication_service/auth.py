#!/usr/bin/env python3
""" This module contains the Auth class"""
from bcrypt import hashpw, gensalt, checkpw
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from user import User
from uuid import uuid4


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

    def create_session(self, email: str) -> str:
        """Create a new session for the user
        """
        try:
            user = self._db.find_user_by(email=email)
            user.session_id = _generate_uuid()
            return user.session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """
        get user from session id
        """
        if session_id:
            try:
                user = self._db.find_user_by(session_id=session_id)
                return user
            except NoResultFound:
                return None
        else:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        destroys a session
        """
        self._db.update_user(user_id, session_id=None)
        return None

    def get_reset_password_token(self, email: str) -> str:
        """Generates a reset password token"""
        try:
            user = self._db.find_user_by(email=email)
            uuid = _generate_uuid()
            user.reset_token = uuid
            return uuid
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_tokon: str, password: str) -> None:
        try:
            user = self._db.find_user_by(reset_tokon=reset_tokon)
            password = _hash_password(password)
            self._db.update_user(
                user.id, hashed_password=password,
                reset_token=None
                )
            return None
        except NoResultFound:
            raise ValueError


def _hash_password(password: str) -> bytes:
    """Hashes a password
    """
    return hashpw(password.encode('utf-8'), gensalt())


def _generate_uuid() -> str:
    """Generates a UUID
    """
    return str(uuid4())
