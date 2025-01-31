#!/usr/bin/env python3
"""Session Authentication Class
"""
from api.v1.auth.auth import Auth
import os
import uuid


class SessionAuth(Auth):
    """Session Authentication Class
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Create a session ID
        """
        if user_id is None:
            return None
        if type(user_id) is not str:
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Return a User ID based on a Session ID
        """
        if session_id is None:
            return None
        if type(session_id) is not str:
            return None
        return self.user_id_by_session_id.get(session_id)

    def session_cookie(self, request=None):
        """Return a session cookie value from a request
        """
        if request is None:
            return None
        _my_session_id = os.getenv('SESSION_NAME')
        return request.cookies.get(_my_session_id)
