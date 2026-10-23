"""Central application configuration."""

# os reads environment variables supplied by Docker Compose.
import os

# python-dotenv can read a local .env file during non-Docker development.
from dotenv import load_dotenv

# Search for a file named .env. Docker Compose variables can also supply these.
load_dotenv()

# This title appears in Swagger UI.
APP_NAME = "CampusCatalog Integration API"

# All user endpoints are grouped under this URL prefix.
API_PREFIX = "/api"

# The database URL includes the driver, credentials, service name, port, and DB.
DATABASE_URL = os.getenv("DATABASE_URL", "")

# LAB BREAKPOINT: the Compose value must eventually match the frontend port.
FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://localhost:5174")
