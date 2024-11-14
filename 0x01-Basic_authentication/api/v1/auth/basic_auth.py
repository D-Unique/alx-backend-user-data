#!/usr/bin/env python3
"""This is the basicauth module"""
from .auth import Auth
import base64
from typing import Tuple, TypeVar
from models.user import User


class BasicAuth(Auth):
    """Implement basic authentication"""
    pass
