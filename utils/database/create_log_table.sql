CREATE TABLE kekbot.chat_log (
    author_id INT NOT NULL,
    author_name VARCHAR(25) NOT NULL,
    is_mod VARCHAR(5) NOT NULL,
    is_sub BOOLEAN NOT NULL,
    is_turbo BOOLEAN NOT NULL,
    message VARCHAR(500) NULL,
    channel VARCHAR(25) NOT NULL,
    message_time TIMESTAMP NOT NULL);