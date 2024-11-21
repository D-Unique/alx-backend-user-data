#!/usr/bin/env python3
""" DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from user import Base, User
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Add a new user to the database.

        Args:
            email (str): The user's email.
            hashed_password (str): The user's hashed password.

        Returns:
            User: The newly created User object.
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """
        Finds a user in the database.

        Args:
            **kwargs: Keyword arguments.

        Returns:
            User: The user found or raise NoResultFound.
        """
        if not kwargs:
            raise InvalidRequestError
        # Ensure only valid column names are passed as filter arguments
        valid_columns = User.__table__.columns.keys()
        for key in kwargs.keys():
            if key not in valid_columns:
                raise InvalidRequestError

        # Query the users table based on the provided keyword arguments
        user = self._session.query(User).filter_by(**kwargs).first()

        if user is None:
            raise NoResultFound

        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Updates a user's attributes in the database.

        Args:
            user_id (int): The ID of the user to update.
            **kwargs: Arbitrary keyword arguments.

        Raises:
            ValueError: If an argument is not valid.
        """
        user = self.find_user_by(id=user_id)

        # Ensure only valid attributes are updated
        valid_columns = User.__table__.columns.keys()
        for key in kwargs.keys():
            if key not in valid_columns:
                raise ValueError(f"Invalid attribute: {key}")

        # Update user's attributes
        for key, value in kwargs.items():
            setattr(user, key, value)

        # Commit the changes to the database
        self._session.commit()
