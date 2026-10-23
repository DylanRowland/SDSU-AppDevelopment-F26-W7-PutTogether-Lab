-- Create the table the FastAPI User model maps to.
CREATE TABLE IF NOT EXISTS users (
    -- SERIAL asks PostgreSQL to generate increasing integer IDs.
    user_id SERIAL PRIMARY KEY,
    -- Usernames must exist and cannot be duplicated.
    username VARCHAR(30) UNIQUE NOT NULL,
    -- Email addresses are required and unique for this small lab.
    email VARCHAR(255) UNIQUE NOT NULL,
    -- The API stores a hash, not the original password.
    password_hash VARCHAR(255) NOT NULL
);

-- Seed one row so the first GET request has something to display.
INSERT INTO users (username, email, password_hash)
VALUES
    ('seeduser', 'seeduser@example.com', 'educational-placeholder-hash')
-- Re-running initialization will not create a duplicate seed username.
ON CONFLICT (username) DO NOTHING;
