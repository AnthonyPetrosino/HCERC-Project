DROP TABLE IF EXISTS posts; -- Deletes any already existing tables named posts

CREATE TABLE posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,   -- A unique int value for each entry
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,   -- Time post was created
    title TEXT NOT NULL,    -- Post title
    content TEXT NOT NULL   -- Post content
);