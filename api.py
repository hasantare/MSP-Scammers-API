from blacksheep import Application, Request
from mspscammers.routes.registration import register_registration_routes
from mspscammers.routes.discord_auth import register_discord_routes
import mspscammers.database as database
import asyncio

app = Application()
register_registration_routes(app=app)
register_discord_routes(app=app)

@app.on_start
async def on_start():
    tasks = [
        database.create_ban_database(),
        database.create_report_database(),
        database.create_user_database()
    ]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    import sys
    from daphne.cli import CommandLineInterface

    CommandLineInterface().run(["api:app"] + sys.argv[1:])
