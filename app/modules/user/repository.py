from sqlalchemy.orm import Session

from .models import Item, User
from .schemas import ItemCreate, UserCreate, UserUpdate


class UserRepository:
    """
    Repository for performing database operations related to `User` and `Item` entities.

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

    def hash_password(self, password: str) -> str:
        """
        Hashes the password using a simplistic approach (for demonstration purposes).

        Parameters
        ----------
        password : str
            The plain text password to hash.

        Returns
        -------
        str
            The hashed password.
        """
        return password

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

    def get_user_by_email(self, email: str):
        """
        Fetches a user by their email.

        Parameters
        ----------
        email : str
            The email of the user to fetch.

        Returns
        -------
        User
            The fetched user object, or None if not found.
        """
        return self.db.query(User).filter(User.email == email).first()

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
        """
        fake_hashed_password = user.password + "notreallyhashed"
        db_user = User(email=user.email, hashed_password=fake_hashed_password)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def get_items(self, skip: int = 0, limit: int = 100):
        """
        Fetches a list of items, implementing pagination.

        Parameters
        ----------
        skip : int, optional
            The number of items to skip (default is 0).
        limit : int, optional
            The maximum number of items to return (default is 100).

        Returns
        -------
        list[Item]
            A list of item objects.
        """
        return self.db.query(Item).offset(skip).limit(limit).all()

    def create_user_item(self, item: ItemCreate, user_id: int):
        """
        Creates a new item for a specified user.

        Parameters
        ----------
        item : ItemCreate
            The schema containing the item's information.
        user_id : int
            The ID of the user who owns the item.

        Returns
        -------
        Item
            The created item object.
        """
        db_item = Item(**item.dict(), owner_id=user_id)
        self.db.add(db_item)
        self.db.commit()
        self.db.refresh(db_item)
        return db_item

    def delete_user(self, user_id: int):
        """
        Deletes a user by their ID.

        Parameters
        ----------
        user_id : int
            The ID of the user to delete.

        Returns
        -------
        None
        """
        self.db.query(User).filter(User.id == user_id).delete()
        self.db.commit()

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
        dict
            A dictionary representing the updated user object.
        """
        db_user = self.db.query(User).filter(User.id == user_id).first()
        if db_user:
            # Update only provided fields
            update_data = user_update.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_user, key, value)

            if 'password' in update_data:
                db_user.hashed_password = self.hash_password(
                    update_data['password']
                )

            self.db.commit()
            self.db.refresh(db_user)
        return {
            "id": db_user.id,
            "email": db_user.email,
            "is_active": db_user.is_active,
        }
