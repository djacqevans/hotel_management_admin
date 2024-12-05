CREATE TABLE IF NOT EXISTS rooms (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    room_type VARCHAR(50) NOT NULL,
    floor INTEGER NOT NULL,
    capacity INTEGER NOT NULL,
    price_per_night DOUBLE PRECISION NOT NULL,
    amenities JSONB NOT NULL
);
