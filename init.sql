\connect cutaway;

CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Создание схемы, если нужна
CREATE SCHEMA IF NOT EXISTS public;

-- Создание таблицы проектов
CREATE TABLE IF NOT EXISTS projects (
    id SERIAL PRIMARY KEY,
    title VARCHAR UNIQUE NOT NULL,
    description VARCHAR NULL,
    link VARCHAR NULL,
    github_link VARCHAR NULL,
    "order" INTEGER NULL DEFAULT 0,
    image_filename VARCHAR NOT NULL
);

-- Создание таблицы пользователей
CREATE TABLE IF NOT EXISTS admins (
    id SERIAL PRIMARY KEY,
    login VARCHAR NOT NULL,
    password VARCHAR NOT NULL
);

-- Вставка начальных данных
INSERT INTO admins (login, password) VALUES
('root', ENCODE(DIGEST('123456', 'sha256'), 'hex'))