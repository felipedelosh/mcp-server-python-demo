-- Tabla users
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    rappi_id VARCHAR(100),
    external_id VARCHAR(100),
    name VARCHAR(200) NOT NULL,
    email VARCHAR(200) UNIQUE NOT NULL,
    phone VARCHAR(50)
);

-- Tabla events
CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    event_id VARCHAR(100) NOT NULL,
    status VARCHAR(10) NOT NULL CHECK (status IN ('OK', 'FAIL')),
    points INTEGER NOT NULL DEFAULT 0,
    date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tabla event_accumulations
CREATE TABLE event_accumulations (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    points INTEGER NOT NULL DEFAULT 0
);

-- Tabla event_redeems
CREATE TABLE event_redeems (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    points INTEGER NOT NULL DEFAULT 0
);
