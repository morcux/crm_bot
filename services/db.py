import pytz
import aiosqlite
from datetime import datetime


class AsyncDatabaseHandler:
    def __init__(self, db_name='database.db'):
        self.db_name = db_name

    async def create_tables(self):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    time TIMESTAMP DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime', '+3 hours')),
                    user_id INTEGER,
                    url TEXT
                )
            ''')

            await db.execute('''
                CREATE TABLE IF NOT EXISTS channels (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    channel_id INTEGER,
                    channel_name TEXT
                )
            ''')

            await db.execute('''
                CREATE TABLE IF NOT EXISTS subscriptions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    url_name TEXT,
                    channel_id INTEGER,
                    timestamp TIMESTAMP DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime', '+3 hours'))
                )
            ''')

            await db.execute('''
                CREATE TABLE IF NOT EXISTS permissions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    channel_id INTEGER
                )
            ''')

            await db.execute('''
                CREATE TABLE IF NOT EXISTS permission_url (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    channel_id INTEGER
                )
            ''')

            await db.execute('''
                CREATE TABLE IF NOT EXISTS urls (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    channel_id INTEGER,
                    url TEXT
                )
            ''')

            await db.commit()

    async def add_user(self, user_id, url):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute('''
                INSERT INTO users (user_id, url) VALUES (?, ?)
            ''', (user_id, url))
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
            await db.execute('''
                INSERT INTO channels (channel_id, channel_name) VALUES (?, ?)
            ''', (channel_id, channel_name))
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

    async def delete_all_users(self):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute('DELETE FROM users')
            await db.commit()

    # Methods for Subscriptions and Permissions

    async def add_subscription(self, user_id, url_name, channel_id):
        moscow_tz = pytz.timezone('Europe/Moscow')
        current_time_msk = datetime.now(moscow_tz).strftime('%Y-%m-%d %H:%M:%S')
        
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute('''
                INSERT INTO subscriptions (user_id, url_name, channel_id, timestamp) VALUES (?, ?, ?, ?)
            ''', (user_id, url_name, channel_id, current_time_msk))
            await db.commit()

    async def get_subscriptions(self, user_id, channel_id=None):
        async with aiosqlite.connect(self.db_name) as db:
            if channel_id:
                cursor = await db.execute('''
                    SELECT url_name, timestamp FROM subscriptions WHERE user_id = ? AND channel_id = ?
                ''', (user_id, channel_id))
            else:
                cursor = await db.execute('''
                    SELECT url_name, timestamp FROM subscriptions WHERE user_id = ?
                ''', (user_id,))
            subscriptions = await cursor.fetchall()
            return subscriptions

    async def delete_subscription(self, user_id, channel_id):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute('''
                DELETE FROM subscriptions WHERE user_id = ? AND channel_id = ?
            ''', (user_id, channel_id))
            await db.commit()

    async def add_permission(self, user_id, channel_id):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute('''
                INSERT INTO permissions (user_id, channel_id) VALUES (?, ?)
            ''', (user_id, channel_id))
            await db.commit()

    async def get_permissions(self, user_id):
        async with aiosqlite.connect(self.db_name) as db:
            cursor = await db.execute('''
                SELECT * FROM permissions WHERE user_id = ?
            ''', (user_id,))
            permissions = await cursor.fetchall()
            return permissions

    async def delete_permission(self, user_id, channel_id):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute('''
                DELETE FROM permissions WHERE user_id = ? AND channel_id = ?
            ''', (user_id, channel_id))
            await db.commit()

    async def get_user_channels(self, user_id):
        async with aiosqlite.connect(self.db_name) as db:
            cursor = await db.execute('''
                SELECT channels.channel_id, channels.channel_name 
                FROM channels 
                INNER JOIN permissions ON channels.channel_id = permissions.channel_id
                WHERE permissions.user_id = ?
            ''', (user_id,))
            channels = await cursor.fetchall()
            return channels

    # Methods for permission_url

    async def add_permission_url(self, user_id, channel_id):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute('''
                INSERT INTO permission_url (user_id, channel_id) VALUES (?, ?)
            ''', (user_id, channel_id))
            await db.commit()

    async def get_permission_urls(self, user_id):
        async with aiosqlite.connect(self.db_name) as db:
            cursor = await db.execute('''
                SELECT * FROM permission_url WHERE user_id = ?
            ''', (user_id,))
            permissions = await cursor.fetchall()
            return permissions

    async def delete_permission_url(self, user_id, channel_id):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute('''
                DELETE FROM permission_url WHERE user_id = ? AND channel_id = ?
            ''', (user_id, channel_id))
            await db.commit()

    async def delete_channel_by_id(self, channel_id):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute('''
                DELETE FROM channels WHERE channel_id = ?
            ''', (channel_id,))
            await db.commit()

    async def get_user_url(self, user_id):
        async with aiosqlite.connect(self.db_name) as db:
            cursor = await db.execute('''
                SELECT channels.channel_id, channels.channel_name 
                FROM channels 
                INNER JOIN permission_url ON channels.channel_id = permission_url.channel_id
                WHERE permission_url.user_id = ?
            ''', (user_id,))
            channels = await cursor.fetchall()
            return channels

    # Methods for URLs table

    async def add_url(self, channel_id, url):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute('''
                INSERT INTO urls (channel_id, url) VALUES (?, ?)
            ''', (channel_id, url))
            await db.commit()

    async def delete_url(self, url):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute('''
                DELETE FROM urls WHERE url = ?
            ''', (url,))
            await db.commit()

    async def get_all_urls(self, channel_id):
        async with aiosqlite.connect(self.db_name) as db:
            cursor = await db.execute('''
                SELECT * FROM urls WHERE channel_id = ?
            ''', (channel_id,))
            urls = await cursor.fetchall()
            return urls
