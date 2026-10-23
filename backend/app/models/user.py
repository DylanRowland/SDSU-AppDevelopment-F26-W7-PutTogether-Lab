"""SQLAlchemy model for one row in the users table."""

# SQLAlchemy column types and ORM mapping helpers.
from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    # SQLAlchemy discovers model classes that inherit from this base.
    pass


class User(Base):
    # Match the table created by database/init.sql.
    __tablename__ = "users"

    # PostgreSQL generates this primary-key value.
    user_id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # These constraints are also enforced by PostgreSQL.
    username: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)

    # Store only a password hash, never the original password.
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
