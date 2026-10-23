"""FastAPI application entry point."""

# FastAPI creates the ASGI application and route decorators.
from fastapi import FastAPI

# Browsers enforce CORS, so this middleware permits the configured frontend.
from fastapi.middleware.cors import CORSMiddleware

# Import shared settings and the users router.
from app.core.config import API_PREFIX, APP_NAME, FRONTEND_ORIGIN
from app.routes.users import router as users_router

# Create the application object that Uvicorn will run.
app = FastAPI(title=APP_NAME)

# LAB BREAKPOINT: the Compose value must eventually match localhost:5173.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root() -> dict[str, str]:
    """Return a health message without querying PostgreSQL."""

    # This proves FastAPI is running, but it does not prove the database works.
    return {"message": "Integration API is running"}


# Mount all user endpoints under /api.
app.include_router(users_router, prefix=API_PREFIX)
