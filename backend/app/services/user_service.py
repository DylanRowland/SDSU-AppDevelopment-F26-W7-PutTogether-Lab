"""Service layer: application rules between routes and repository."""

# HTTPException communicates a missing user as HTTP 404.
from fastapi import HTTPException

# PasswordHash provides a safe password hashing implementation.
from pwdlib import PasswordHash

from app.models.user import User
from app.repository.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate


# Select pwdlib's recommended password-hashing algorithm.
password_hasher = PasswordHash.recommended()


class UserService:
    def __init__(self, repository: UserRepository):
        # Keep database details out of the route functions.
        self.repository = repository

    def create_user(self, data: UserCreate) -> User:
        # Convert validated request data into the database model.
        user = User(
            username=data.username,
            email=str(data.email),
            # Hash the password before it reaches PostgreSQL.
            password_hash=password_hasher.hash(data.password),
        )
        # Ask the repository to persist the model.
        return self.repository.create(user)

    def list_users(self) -> list[User]:
        # Read all users through the repository.
        return self.repository.get_all()

    def get_user(self, user_id: int) -> User:
        # Ask the repository for the requested row.
        user = self.repository.get_by_id(user_id)
        if user is None:
            # Turn a missing row into a useful HTTP response.
            raise HTTPException(status_code=404, detail="User not found")
        return user

    def update_user(self, user_id: int, data: UserUpdate) -> User:
        # Reuse the not-found rule before changing anything.
        user = self.get_user(user_id)
        user.username = data.username
        user.email = str(data.email)
        # Hash the replacement password instead of storing it directly.
        user.password_hash = password_hasher.hash(data.password)
        return self.repository.update(user)

    def delete_user(self, user_id: int) -> None:
        # Find the row first so nonexistent IDs receive HTTP 404.
        user = self.get_user(user_id)
        self.repository.delete(user)
