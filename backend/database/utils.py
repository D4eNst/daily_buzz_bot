import sqlite3 as sq
from .models import User, Subscribe

conn = sq.connect("backend/database/database.db")
cursor = conn.cursor()


def connect() -> None:
    cursor.execute("""CREATE TABLE IF NOT EXISTS users(
    tg_id INTEGER PRIMARY KEY,
    balance INTEGER DEFAULT 0,
    total_buy INTEGER DEFAULT 0,
    status INTEGER DEFAULT 1,
    subscribe BOOL DEFAULT FALSE,
    subscribe_date INTEGER,
    subscribe_period INTEGER
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
    cursor.execute("""
            INSERT INTO users(tg_id)
            VALUES(?)
        """, (user.tg_id, ))
    conn.commit()
    pass


def get_user(user_id) -> User or None:
    cursor.execute("""SELECT * FROM users WHERE tg_id==?""", (user_id,))
    res = cursor.fetchone()
    if not res:
        return None
    else:
        values_list = list(res)
        values_list[4] = True if values_list[4] else False
        user = User(*values_list)
        return user


def update_user(user) -> None:
    cursor.execute("""UPDATE users SET
    balance = ?,
    total_buy = ?,
    status = ?,
    subscribe = ?,
    subscribe_date = ?,
    subscribe_period = ? WHERE tg_id = ?
    """, user.get_values())
    conn.commit()
    pass


def del_user(user) -> None:
    conn.commit()
    pass


def add_subscribe(sub) -> None:
    conn.commit()
    pass


def get_subscribe(sub_id) -> Subscribe or None:
    cursor.execute("""SELECT * FROM subscribes WHERE id==?""", (sub_id,))
    res = cursor.fetchone()
    if not res:
        return None
    else:
        sub = Subscribe(*res)
        return sub


def get_subscribes() -> list:
    cursor.execute("""SELECT * FROM subscribes""")
    res = cursor.fetchall()
    subs = []
    for i in res:
        sub = Subscribe(*i)
        subs.append(sub)
    return subs


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
