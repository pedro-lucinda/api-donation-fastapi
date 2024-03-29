from sqlalchemy.orm import Session

from .models import Item, User
from .schemas import ItemCreate, UserCreate, UserUpdate


class UserRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def hash_password(self, password: str) -> str:
        return password

    def get_user(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()

    def get_user_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()

    def get_users(self, skip: int = 0, limit: int = 100):
        return self.db.query(User).offset(skip).limit(limit).all()

    def create_user(self, user: UserCreate):
        fake_hashed_password = user.password + "notreallyhashed"
        db_user = User(email=user.email, hashed_password=fake_hashed_password)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def get_items(self, skip: int = 0, limit: int = 100):
        return self.db.query(Item).offset(skip).limit(limit).all()

    def create_user_item(self, item: ItemCreate, user_id: int):
        db_item = Item(**item.model_dump(), owner_id=user_id)
        self.db.add(db_item)
        self.db.commit()
        self.db.refresh(db_item)
        return db_item

    def delete_user(self, user_id: int):
        self.db.query(User).filter(User.id == user_id).delete()
        self.db.commit()

    def update_user(self, user_id: int, user_update: UserUpdate):
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
