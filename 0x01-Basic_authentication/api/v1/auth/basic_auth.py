#!/usr/bin/env python3
"""This is the basicauth module"""
from .auth import Auth
import base64
from typing import Tuple, TypeVar
from models.user import User


class BasicAuth(Auth):
    """Implement basic authentication"""
    

    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """This function extract the base64 part of authorization header"""
        if authorization_header is None or not isinstance(authorization_header, str):
            return None
        dc = authorization_header.startswith('Basic ')
        if not dc:
            return None
        else:
            [basic, byt] = authorization_header.split(' ', 1)
            return byt
