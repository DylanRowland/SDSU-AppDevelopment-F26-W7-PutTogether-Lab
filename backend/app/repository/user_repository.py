"""Repository layer: database operations only."""

# select builds a SQL SELECT statement; Session executes database work.
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:
    def __init__(self, db: Session):
        # Save the request's session so each method can use it.
        self.db = db

    def create(self, user: User) -> User:
        # Stage the new object for insertion.
        self.db.add(user)
        # Send INSERT to PostgreSQL.
        self.db.commit()
        # Reload generated values such as user_id.
        self.db.refresh(user)
        # Return the saved model to the service layer.
        return user

    def get_all(self) -> list[User]:
        # Order results so the response is predictable for the lab.
        return list(self.db.scalars(select(User).order_by(User.user_id)))

    def get_by_id(self, user_id: int) -> User | None:
        # Look up one row by its primary key.
        return self.db.get(User, user_id)

    def update(self, user: User) -> User:
        # The service changed the object; commit sends those changes.
        self.db.commit()
        # Refresh the object from PostgreSQL.
        self.db.refresh(user)
        return user

    def delete(self, user: User) -> None:
        # Mark the row for deletion and commit the DELETE statement.
        self.db.delete(user)
        self.db.commit()
