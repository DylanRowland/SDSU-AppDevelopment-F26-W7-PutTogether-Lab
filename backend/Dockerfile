# Start with a small Linux image that already contains Python 3.12.
FROM python:3.12-slim

# All following paths are relative to /app inside the image.
WORKDIR /app

# Copy dependencies first so Docker can reuse this layer when app code changes.
COPY requirements.txt .

# Install FastAPI, SQLAlchemy, the Postgres driver, and supporting libraries.
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application package into the image.
COPY app ./app

# Document the port the Uvicorn process listens on inside the container.
EXPOSE 8000

# Start FastAPI on every container interface so Docker can publish it.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
