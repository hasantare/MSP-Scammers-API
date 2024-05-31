from blacksheep import Application, Request
from blacksheep.server.responses import json
from mspscammers import database as db
from typing import Awaitable, Callable

from typing import Dict, Awaitable, Callable

class DatabaseCache:
    _cache: Dict[str, Dict[str, bool]]

    def __init__(self):
        self._cache = {}

    async def check_username_exists_cached(self, username: str) -> bool:
        if "username" not in self._cache:
            self._cache["username"] = {}

        if username not in self._cache["username"]:
            self._cache["username"][username] = await db.check_username_exists(username)

        return self._cache["username"][username]

    async def check_user_exists_cached(self, user_id: str) -> bool:
        if "user_id" not in self._cache:
            self._cache["user_id"] = {}

        if user_id not in self._cache["user_id"]:
            self._cache["user_id"][user_id] = await db.check_user_exists(user_id)

        return self._cache["user_id"][user_id]
    
    def update_cache(self, user_id: str, username: str) -> None:
        if "username" not in self._cache:
            self._cache["username"] = {}
        if "user_id" not in self._cache:
            self._cache["user_id"] = {}
        self._cache["username"][username] = True
        self._cache["user_id"][user_id] = True

cache  = DatabaseCache()

async def create_account(request: Request) -> Awaitable[json]:
    data: dict = await request.json()

    required_fields = ['discord_user_id', 'discord_username', 'image_url']
    missing_fields = [{"loc": [field], "msg": f"Field '{field}' is required", "type": "value_error"} for field in required_fields if field not in data]
    if missing_fields:
        error_response = {"detail": missing_fields}
        return json(data=error_response, status=400)

    username_exists = await cache.check_username_exists_cached(data['discord_username'])
    user_exists = await cache.check_user_exists_cached(data['discord_user_id'])

    if username_exists:
        error_response = {
            "detail": [
                {
                    "loc": ["username"],
                    "msg": f"Username '{data['discord_username']}' already exists",
                    "type": "value_error"
                }]
            }
        return json(data=error_response, status=409)
    elif user_exists:
        error_response = {
            "detail": [
                {
                    "loc": ["discord_user_id"],
                    "msg": f"Discord user ID '{str(data['discord_user_id'])}' already exists",
                    "type": "value_error"
                }
            ]
        }
        return json(data=error_response, status=409)

    await db.add_user(data['discord_user_id'], request.client_ip, data['discord_username'], data['image_url'])
    user_data = await db.get_user_data_json(data['discord_user_id'])

    if user_data:
        cache.update_cache(user_id=data['discord_user_id'], username=data['discord_username'])

    if user_data:
        success_response = {
            'success': True,
            'message': 'Account created successfully',
            'user_data': user_data
        }
        return json(data=success_response, status=201)
    else:
        error_response = {
            'error': 'Internal Server Error',
            'message': 'Failed to create account'
        }
        return json(data=error_response, status=500)

def register_registration_routes(app: Application) -> None:
    app.router.add_post("/api/v1/registration/create", create_account)
