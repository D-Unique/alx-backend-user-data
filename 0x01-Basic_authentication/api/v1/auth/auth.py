#!/usr/bin/env python3
"""This is the authantication module"""
from flask import request
from typing import TypeVar


class Auth:
    """The Auth class"""

    def __init__():
        pass

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """this function checks if the path requires auth"""
        return False

    def authorization_header(self, request=None) -> str:
        """the function returns the auth header for a request"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """this function returns the current users"""
        return None
