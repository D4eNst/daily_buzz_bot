import sqlite3 as sq
from models import User, Subscribe

conn = sq.connect("backend/database/database.db")
cursor = conn.cursor()


def connect() -> None:
    cursor.execute("""CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tg_id INTEGER UNIQUE,
    balance INTEGER,
    total_buy INTEGER,
    status INTEGER,
    subscribe BOOL
    subscribe_date TEXT DEFAULT NONE,
    subscribe_period INTEGER DEFAULT NONE
    )""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS subscribes(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    period INTEGER,
    price INTEGER
    )""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS history(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tg_id INTEGER,
        sub_id INTEGER
        )""")
    print("database has been started successful")
    conn.commit()


def close() -> None:
    conn.close()


def add_user(user) -> None:
    conn.commit()
    pass


def get_user(tg_id) -> None:
    conn.commit()
    pass


def update_user(user) -> None:
    conn.commit()
    pass


def del_user(user) -> None:
    conn.commit()
    pass


def add_subscribe(sub) -> None:
    conn.commit()
    pass


def get_subscribe(sub_id) -> None:
    conn.commit()
    pass


def update_subscribe(sub) -> None:
    conn.commit()
    pass


def del_subscribe(sub) -> None:
    conn.commit()
    pass


def add_history() -> None:
    conn.commit()
    pass


def get_history() -> None:
    conn.commit()
    pass


def update_history() -> None:
    conn.commit()
    pass


def del_history() -> None:
    conn.commit()
    pass
