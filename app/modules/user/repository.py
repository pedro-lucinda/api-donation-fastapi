from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from .models import User
from .schemas import UserCreate, UserUpdate

from sqlalchemy.exc import SQLAlchemyError


class UserRepository:
    """
    Repository for performing database operations related to `User` entity.

    Attributes
    ----------
    db : Session
        The SQLAlchemy database session used for database operations.
    """

    def __init__(self, db: Session) -> None:
        """
        Initializes the UserRepository with the given database session.

        Parameters
        ----------
        db : Session
            The SQLAlchemy session to use for database operations.
        """
        self.db = db

    def get_user(self, user_id: int):
        """
        Fetches a user by their ID.

        Parameters
        ----------
        user_id : int
            The ID of the user to fetch.

        Returns
        -------
        User
            The fetched user object, or None if not found.
        """
        return self.db.query(User).filter(User.id == user_id).first()

    def get_users(self, skip: int = 0, limit: int = 100):
        """
        Fetches a list of users, implementing pagination.

        Parameters
        ----------
        skip : int, optional
            The number of users to skip (default is 0).
        limit : int, optional
            The maximum number of users to return (default is 100).

        Returns
        -------
        list[User]
            A list of user objects.
        """
        return self.db.query(User).offset(skip).limit(limit).all()

    def get_user_by_email(self, email: str):
        """
        Fetches a user by their email address.

        Parameters
        ----------
        email : str
            The email address of the user to fetch.
        
        Returns
        -------
        User
            The fetched user object, or None if not found.
        
        Raises
        ------
        HTTPException
            If there is an issue with the database query.
        """
        try:
            return self.db.query(User).filter(User.email == email).first()
        except SQLAlchemyError as e:
            print(e)
            self.db.rollback()
            raise HTTPException(status_code=500, detail="Database query failed") from e

    def create_user(self, user: UserCreate):
        """
        Creates a new user in the database.

        Parameters
        ----------
        user : UserCreate
            The schema containing the user's information.
        
        Returns
        -------
        User
            The created user object.
        
        Raises
        ------
        HTTPException
            If the email is already registered.
        """
        try:
            existing_user = self.get_user_by_email(user.email)
            if existing_user:
                raise HTTPException(status_code=400, detail="Email is already registered")

            db_user = User(**user.dict())
            self.db.add(db_user)
            self.db.commit()
            self.db.refresh(db_user)
            return db_user
        except SQLAlchemyError as e:
            print(e)
            self.db.rollback()
            raise HTTPException(status_code=500, detail="Database transaction failed")
        except HTTPException as http_exc:
            self.db.rollback()
            raise http_exc
        finally:
            self.db.close()

    def update_user(self, user_id: int, user_update: UserUpdate):
        """
        Updates a user's information by their ID.

        Parameters
        ----------
        user_id : int
            The ID of the user to update.
        user_update : UserUpdate
            The schema containing the user's updated information.

        Returns
        -------
        User
            The updated user object.
        """
        db_user = self.get_user(user_id)
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")

        update_data = user_update.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(db_user, key, value)

        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def get_user_by_id(self, user_id: int):
        """
        Fetches a user by their ID.

        Parameters
        ----------
        user_id : int
            The ID of the user to fetch.

        Returns
        -------
        User
            The fetched user object, or None if not found.
        """
        return self.db.query(User).filter(User.id == user_id).first()

    def deleteAll(self):
        """
        Deletes all users from the database.

        Returns
        -------
        None
        """
        self.db.query(User).delete()
        self.db.commit()
        return None