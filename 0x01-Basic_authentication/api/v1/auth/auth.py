#!/usr/bin/env python3
"""This is the authantication module"""
from flask import request
from typing import TypeVar, List


class Auth:
    """The Auth class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """this function checks if the path requires auth"""
        if path is None:
            return True
        if len(excluded_paths) <= 0 or excluded_paths is None:
            return True
        if not path.endswith('/'):
            path = path + '/'
        if path not in excluded_paths:
            return True
        return False

    def authorization_header(self, request=None) -> str:
        """the function returns the auth header for a request"""
        if request is None:
            return None
        authorization_header = request.headers.get('Authorization', None)
        """if authorization_header is None:
            return None"""
        return authorization_header

    def current_user(self, request=None) -> TypeVar('User'):
        """this function returns the current users"""
        return None
