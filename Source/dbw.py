import aiosqlite
import asyncio
from datetime import datetime


async def create_table(table_name):
    async with aiosqlite.connect(table_name) as db:
        await db.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            username TEXT,
            last_interaction TIMESTAMP
        )
        ''')
        await db.commit()


async def add_user(table_name, user_id, username):
    async with aiosqlite.connect(table_name) as db:
        await db.execute('''
        INSERT INTO users (user_id, username, last_interaction)
        VALUES (?, ?, ?)
        ''', (user_id, username, datetime.now()))
        await db.commit()


async def view_database(table_name):
    async with aiosqlite.connect(table_name) as db:
        cursor = await db.execute('SELECT * FROM users')
        users_new = await cursor.fetchall()
        for u in users_new:
            print(u)  # Выводим данные о пользователях в консоль
        return users_new  # Возвращаем данные для дальнейшей обработки


async def update_user(table_name, user_id, new_username=None):
    async with aiosqlite.connect(table_name) as db:
        # Обновление имени пользователя и времени последнего взаимодействия
        if new_username:
            await db.execute('''
            UPDATE users
            SET username = ?, last_interaction = ?
            WHERE user_id = ?
            ''', (new_username, datetime.now(), user_id))
        else:
            await db.execute('''
            UPDATE users
            SET last_interaction = ?
            WHERE user_id = ?
            ''', (datetime.now(), user_id))
        await db.commit()


async def delete_user(table_name, user_id):
    async with aiosqlite.connect(table_name) as db:
        await db.execute('''
        DELETE FROM users WHERE user_id = ?
        ''', (user_id,))
        await db.commit()


async def get_username_by_user_id(table_name, user_id):
    async with aiosqlite.connect(table_name) as db:
        cursor = await db.execute('SELECT username FROM users WHERE user_id = ?', (user_id,))
        row = await cursor.fetchone()
        if row:
            return row[0]  # Возвращаем значение имени пользователя
        return None  # Если пользователь не найден, возвращаем None


