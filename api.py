from blacksheep import Application, Request
from mspscammers.routes.registration import register_registration_routes
from mspscammers.routes.discord_auth import register_discord_routes
from mspscammers.routes.reporting import register_reporting_routes
import mspscammers.database as database
import asyncio

app = Application()
register_registration_routes(app=app)
register_discord_routes(app=app)
register_reporting_routes(app=app)

@app.on_start
async def on_start():
    await database.create_ban_database(),
    await database.create_report_database(),
    await database.create_user_database()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app=app, host="127.0.0.1", port=8000)
