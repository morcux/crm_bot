import pytz
import aiosqlite
from datetime import datetime


class AsyncDatabaseHandler:
    def __init__(self, db_name='database.db'):
        self.db_name = db_name

    async def create_tables(self):
        async with aiosqlite.connect(self.db_name) as db:
            cursor = await db.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    time TIMESTAMP DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime', '+3 hours')),
                    user_id INTEGER,
                    url TEXT
                )
            ''')
            await cursor.close()

            cursor = await db.execute('''
                CREATE TABLE IF NOT EXISTS channels (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    channel_id INTEGER,
                    channel_name TEXT
                )
            ''')
            await cursor.close()


    async def add_user(self, user_id, url):
        async with aiosqlite.connect(self.db_name) as db:
            cursor = await db.execute('''
                INSERT INTO users (user_id, url) VALUES (?, ?)
            ''', (user_id, url))
            await cursor.close()
            await db.commit()

    async def check_user_by_id(self, user_id):
        async with aiosqlite.connect(self.db_name) as db:
            cursor = await db.execute('''
                SELECT url, time FROM users WHERE user_id = ?
            ''', (user_id,))
            user_info = await cursor.fetchone()

            if user_info:
                url, user_time = user_info
                moscow_tz = pytz.timezone('Europe/Moscow')
                current_time_msk = datetime.now(moscow_tz)
                user_time = datetime.fromisoformat(user_time).astimezone(moscow_tz)

                delta = current_time_msk.date() == user_time.date()
                if delta:
                    return url
                else:
                    return None

            return None

    async def add_channel(self, channel_id, channel_name):
        async with aiosqlite.connect(self.db_name) as db:
            cursor = await db.execute('''
                INSERT INTO channels (channel_id, channel_name) VALUES (?, ?)
            ''', (channel_id, channel_name))
            await cursor.close()
            await db.commit()

    async def delete_user_by_id(self, user_id):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute('''
                DELETE FROM users WHERE user_id = ?
            ''', (user_id,))
            await db.commit()

    async def get_all_channels(self):
        async with aiosqlite.connect(self.db_name) as db:
            cursor = await db.execute('''
                SELECT * FROM channels
            ''')
            channels = await cursor.fetchall()
            return channels

    async def close_connection(self):
        pass
    

    async def delete_all_users(self):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute('DELETE FROM users')
            await db.commit()