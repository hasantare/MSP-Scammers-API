import aiosqlite
import secrets
import string
from datetime import datetime

from mspscammers.token_manager.authtoken import AuthtokenManager

async def create_user_database():
    async with aiosqlite.connect('databases/users.db') as db:
        async with db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                discord_user_id TEXT PRIMARY KEY,
                auth_token TEXT,
                ip_address TEXT,
                discord_username TEXT,
                image_url TEXT
            )
        '''):
            pass

async def create_report_database():
    async with aiosqlite.connect('databases/reports.db') as db:
        async with db.execute('''
            CREATE TABLE IF NOT EXISTS reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                description TEXT,
                discord_user_id TEXT,
                ip_address TEXT,
                scammer_id TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        '''):
            pass

async def create_ban_database():
    async with aiosqlite.connect('databases/bans.db') as db:
        async with db.execute('''
            CREATE TABLE IF NOT EXISTS bans (
                discord_user_id TEXT PRIMARY KEY,
                banned_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                reason TEXT
            )
        '''):
            pass

async def get_user_data(discord_user_id):
    async with aiosqlite.connect('databases/users.db') as db:
        async with db.execute('''
            SELECT *
            FROM users
            WHERE discord_user_id = ?
        ''', (discord_user_id,)) as cursor:
            return await cursor.fetchone()

async def get_user_data_json(discord_user_id):
    async with aiosqlite.connect('databases/users.db') as db:
        async with db.execute('''
            SELECT *
            FROM users
            WHERE discord_user_id = ?
        ''', (discord_user_id,)) as cursor:
            user_data = await cursor.fetchone()
            if user_data:
                user_json = {
                    'discord_user_id': user_data[0],
                    'auth_token': user_data[1],
                    'discord_username': user_data[3],
                    'image_url': user_data[4]
                }
                return user_json
            else:
                return None
            
async def add_user(discord_user_id, ip_address, discord_username, image_url):
    auth_token = AuthtokenManager.create_auth_token(str(discord_user_id))
    async with aiosqlite.connect('databases/users.db') as db:
        await db.execute('''
            INSERT OR REPLACE INTO users (discord_user_id, auth_token, ip_address, discord_username, image_url)
            VALUES (?, ?, ?, ?, ?)
        ''', (discord_user_id, auth_token, ip_address, discord_username, image_url))
        await db.commit()
    return auth_token

async def check_user_exists(discord_user_id):
    async with aiosqlite.connect('databases/users.db') as db:
        async with db.execute('''
            SELECT COUNT(*) AS count
            FROM users
            WHERE discord_user_id = ?
        ''', (discord_user_id,)) as cursor:
            count = await cursor.fetchone()
            return count[0] > 0

async def add_report(username, scammer_id, description, discord_user_id, ip_address):
    async with aiosqlite.connect('databases/reports.db') as db:
        await db.execute('''
            INSERT INTO reports (username, description, discord_user_id, ip_address, scammer_id)
            VALUES (?, ?, ?, ?, ?)
        ''', (username, description, discord_user_id, ip_address, scammer_id))
        await db.commit()

async def check_ip_auth(ip_address, auth_token):
    async with aiosqlite.connect('databases/users.db') as db:
        async with db.execute('''
            SELECT ip_address
            FROM users
            WHERE ip_address = ? AND auth_token = ?
        ''', (ip_address, auth_token)) as cursor:
            return (await cursor.fetchone()) is not None

async def check_username_exists(discord_username):
    async with aiosqlite.connect('databases/users.db') as db:
        async with db.execute('''
            SELECT COUNT(*) AS count
            FROM users
            WHERE discord_username = ?
        ''', (discord_username,)) as cursor:
            count = await cursor.fetchone()
            return count[0] > 0

async def has_reported(auth_token, scammer_id):
    async with aiosqlite.connect('databases/users.db') as user_db:
        async with aiosqlite.connect('databases/reports.db') as report_db:
            async with user_db.execute('''
                SELECT discord_user_id
                FROM users
                WHERE auth_token = ?
            ''', (auth_token,)) as user_cursor:
                user_row = await user_cursor.fetchone()
                if user_row is None:
                    return False
                async with report_db.execute('''
                    SELECT COUNT(*) AS count
                    FROM reports
                    WHERE discord_user_id = ? AND scammer_id = ?
                ''', (user_row[0], scammer_id)) as report_cursor:
                    report_row = await report_cursor.fetchone()
                    return report_row[0] > 0

async def get_discord_user_id(auth_token):
    async with aiosqlite.connect('databases/users.db') as db:
        async with db.execute('''
            SELECT discord_user_id
            FROM users
            WHERE auth_token = ?
        ''', (auth_token,)) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else None

async def get_total_reports_for_scammer(scammer_id):
    async with aiosqlite.connect('databases/reports.db') as db:
        async with db.execute('''
            SELECT COUNT(*) AS count
            FROM reports
            WHERE scammer_id = ?
        ''', (scammer_id,)) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else 0

async def get_all_reports():
    async with aiosqlite.connect('databases/reports.db') as db:
        async with db.execute('''
            SELECT *
            FROM reports
            ORDER BY created_at DESC
        ''') as cursor:
            return await cursor.fetchall()

async def get_user_data_from_ip(ip_address):
    async with aiosqlite.connect('databases/users.db') as db:
        async with db.execute('''
            SELECT *
            FROM users
            WHERE ip_address = ?
        ''', (ip_address,)) as cursor:
            return await cursor.fetchone()

async def ban_user(discord_user_id, reason):
    async with aiosqlite.connect('databases/bans.db') as db:
        await db.execute('''
            INSERT OR REPLACE INTO bans (discord_user_id, reason)
            VALUES (?, ?)
        ''', (discord_user_id, reason))
        await db.commit()

async def is_user_banned(discord_user_id):
    async with aiosqlite.connect('databases/bans.db') as db:
        async with db.execute('''
            SELECT COUNT(*) AS count
            FROM bans
            WHERE discord_user_id = ?
        ''', (discord_user_id,)) as cursor:
            row = await cursor.fetchone()
            return row[0] > 0

async def unban_user(discord_user_id):
    async with aiosqlite.connect('databases/bans.db') as db:
        await db.execute('''
            DELETE FROM bans
            WHERE discord_user_id = ?
        ''', (discord_user_id,))
        await db.commit()