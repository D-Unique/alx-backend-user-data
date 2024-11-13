#!/usr/bin/env python3
"""This is the basicauth module"""
from .auth import Auth
import base64
from typing import Tuple
from ....models.user import User


class BasicAuth(Auth):
    """Implement basic authentication"""

    def decode_base64_authorization_header(
            self, base64_authorization_header: str
            ) -> str:
        """Decodes a Base64-encoded authorization header.

        Args:
            base64_authorization_header: The
            Base64-encoded authorization header.

        Returns:
            The decoded string, or None if the header is invalid.
        """

        if not base64_authorization_header or \
                not isinstance(base64_authorization_header, str):
            return None

        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except (TypeError, ValueError, UnicodeDecodeError):
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str
            ) -> (str, str):
        if not decoded_base64_authorization_header or \
                not isinstance(decoded_base64_authorization_header, str) or \
                ':' not in decoded_base64_authorization_header:
            return None
        else:
            email, pw = decoded_base64_authorization_header.split(':', 1)
            return f"{email}:{pw}"

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str
                                     ) -> TypeVar('User'):
        """Retrieves a User instance based on
        email and password.

        Args:
        user_email: The user's email address.
        user_password: The user's password.

        Returns:
        The User instance if credentials are valid, otherwise None.
        """

        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        users = User.search({'email': user_email})
        if not users:
            return None
        user = users[0]

        valid = User.is_valid_password(user, user_pwd)
        if not valid:
            return None
        return user
