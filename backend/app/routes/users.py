"""HTTP routes for the users CRUD operations."""

# APIRouter groups related endpoints; Depends provides shared dependencies.
from fastapi import APIRouter, Depends, status

# The database session is synchronous, so routes receive a SQLAlchemy Session.
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repository.user_repository import UserRepository
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.services.user_service import UserService


# The main application adds /api, producing paths such as /api/users.
router = APIRouter(prefix="/users", tags=["Users"])


def get_service(db: Session = Depends(get_db)) -> UserService:
    # FastAPI supplies db, then the route receives a service with its repository.
    return UserService(UserRepository(db))


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(data: UserCreate, service: UserService = Depends(get_service)):
    # POST creates a row and returns the safe response model.
    return service.create_user(data)


@router.get("", response_model=list[UserResponse])
def list_users(service: UserService = Depends(get_service)):
    # GET without an ID returns every user.
    return service.list_users()


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, service: UserService = Depends(get_service)):
    # GET with an ID returns one user.
    return service.get_user(user_id)


@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, data: UserUpdate, service: UserService = Depends(get_service)):
    # PUT replaces the editable fields for one user.
    return service.update_user(user_id, data)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, service: UserService = Depends(get_service)):
    # DELETE removes one row and returns HTTP 204 with no response body.
    service.delete_user(user_id)
