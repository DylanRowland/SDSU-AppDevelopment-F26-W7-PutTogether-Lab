# Week 7 Integration Starter — Commented Teaching Version

This starter project contains four pieces that students already learned separately:

- `frontend/`: React + Vite + TypeScript
- `backend/`: FastAPI with the previous core/models/repository/routes/schemas/services structure
- `database/`: PostgreSQL initialization SQL
- `cloudflare/`: Wrangler/Hyperdrive placeholder files for the later cloud discussion

The project is intentionally disconnected at the beginning of the lab. Each piece can be inspected and started, but the complete request is expected to fail until students repair the connection points. The hand-written source and configuration files contain comments explaining what the important lines do.

Generated dependency manifests such as `frontend/package-lock.json` and strict JSON configuration files are left in their valid machine-readable format. Their purpose is explained here rather than inserting invalid JSON comments.

The feature is intentionally small: one `users` table and four operations: create, read, update, and delete. The fields are `user_id`, `username`, `email`, and `password_hash`. The client sends a password, but the API never returns the password or its hash.

## Deliberate lab breakpoints

1. The frontend points at `http://localhost:8001`, while the backend is published on port `8000`.
2. The backend CORS list allows `http://localhost:5174`, while the frontend runs on `5173`.
3. The Docker backend environment uses the wrong PostgreSQL hostname: `postgresql` instead of the Compose service name `postgres`.
4. The backend database session raises a clear error until `DATABASE_URL` is corrected and the database is reachable.
5. The frontend starts with a disconnected status message and its first read request fails until the API connection is repaired.

These are intentional teaching breakpoints, not accidental bugs. The completed version should make this request work:

```text
React form -> FastAPI CRUD route -> PostgreSQL users table -> JSON response -> React page
```

## Run each piece separately

### Frontend

```powershell
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`.

### Backend

```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```

Open `http://127.0.0.1:8000/docs`.

The health check works. The create request is intentionally not connected to the database yet.

### PostgreSQL

From the project root:

```powershell
docker compose up postgres
```

The database is published on `localhost:5432`. The initialization script creates the `users` table.

### Full prepared stack

```powershell
docker compose up --build
```

The containers start, but the complete browser-to-database request is intentionally broken. The lab begins by locating and fixing the five breakpoints above.

## Cloudflare note

The `cloudflare/` folder is a later deployment bridge. D1 is Cloudflare's SQLite database, not PostgreSQL. The Wrangler files here describe a Hyperdrive connection placeholder for a PostgreSQL provider; they are not required to run this local Docker lab.

Do not put a real database password in `wrangler.toml`, React code, or Git. Use local `.env` files and deployment secrets.
