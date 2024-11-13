#!/usr/bin/env python3
"""This is the authantication module"""
from flask import Request
from typing import TypeVar, List


class Auth:
    """The Auth class"""

    def __init__():
        pass

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """this function checks if the path requires auth"""
        if (path not in excluded_paths or
                excluded_paths is None or path is None):
            return True
        return False

    def authorization_header(self, request=None) -> str:
        """the function returns the auth header for a request"""
        authorization_header = request.headers.get('Authorization')
        if request is None or authorization_header is None:
            return None
        return authorization_header

    def current_user(self, request=None) -> TypeVar('User'):
        """this function returns the current users"""
        return None
