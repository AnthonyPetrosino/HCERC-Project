DROP TABLE IF EXISTS posts; -- Deletes any already existing tables named posts

CREATE TABLE posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,   -- A unique int value for each entry
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,   -- Time post was created
    user TEST NOT NULL,     -- User who created
    title TEXT NOT NULL,    -- Post title
    content TEXT NOT NULL,  -- Post content
    ticker TEXT NOT NULL,    -- Post ticker
    price_at_creation DOUBLE NOT NULL   -- Ticker price at post creation ADDED LINE
);