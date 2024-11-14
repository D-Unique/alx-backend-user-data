#!/usr/bin/env python3
"""This is the basicauth module"""
from .auth import Auth
import base64
from typing import Tuple, TypeVar
from models.user import User


class BasicAuth(Auth):
    """Implement basic authentication"""

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """This function extract the base64 part of authorization header"""
        if authorization_header is None or not isinstance(
                authorization_header, str):
            return None
        dc = authorization_header.startswith('Basic ')
        if not dc:
            return None
        else:
            [basic, byt] = authorization_header.split(' ', 1)
            return byt

    def decode_base64_authorization_header(
            self, base64_authorization_header: str
            ) -> str:
        """Decodes a Base64-encoded authorization header.

        Args:
            base64_authorization_header: The
            Base64-encoded authorization header.

        Returns:
            The decoded string, or None if the header is invalid."""

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
        """this method extract credentials"""
        if not decoded_base64_authorization_header or \
                not isinstance(decoded_base64_authorization_header, str) or \
                ':' not in decoded_base64_authorization_header:
            return (None, None)
        else:
            email, pw = decoded_base64_authorization_header.split(':', 1)
            return f"({email}, {pw})"
