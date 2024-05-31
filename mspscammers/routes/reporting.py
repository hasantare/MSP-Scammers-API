from blacksheep import Application, Request, Response
from blacksheep.server.responses import json
from blacksheep.server.authorization import auth
from mspscammers.database import (
    check_ip_auth, get_discord_user_id, has_reported,
    add_report, get_total_reports_for_scammer
)
from typing import Dict

auth_token_cache: Dict[str, str] = {}

async def validate_auth_token(request: Request) -> bool:
    auth_token = request.headers.get_first(b'authorization')
    if not auth_token:
        await unauthorized(request, 'Authentication token is missing')
        return False

    auth_token = auth_token.decode('utf-8')
    if auth_token not in auth_token_cache:
        is_valid = await check_ip_auth(request.client_ip, auth_token)
        if not is_valid:
            await unauthorized(request, "Authentication token doesn't match IP address")
            return False
        auth_token_cache[auth_token] = request.client_ip
    else:
        if auth_token_cache[auth_token] != request.client_ip:
            await unauthorized(request, "Authentication token doesn't match IP address")
            return False

    request.discordid = await get_discord_user_id(auth_token)
    return True

async def validate_request(request: Request, required_fields: list) -> bool:
    data = await request.json()
    for field in required_fields:
        if field not in data:
            await bad_request(request, f"Missing required field: {field}")
            return False
    return True

async def unauthorized(request: Request, message: str) -> Response:
    return json({
        "detail": [
            {
                "loc": ["header", "authorization"],
                "msg": message,
                "type": "value_error"
            }
        ]
    }, status=401)

async def bad_request(request: Request, message: str) -> Response:
    return json({
        "detail": [
            {
                "loc": ["body"],
                "msg": message,
                "type": "value_error"
            }
        ]
    }, status=400)

async def conflict(request: Request, message: str) -> Response:
    return json({
        "detail": [
            {
                "loc": ["body"],
                "msg": message,
                "type": "value_error.conflict"
            }
        ]
    }, status=409)

async def success(request: Request, message: str, data: dict) -> Response:
    return json({
        "success": True,
        "message": message,
        **data
    }, status=200)

async def report_user(request: Request):
    try:
        if not await validate_auth_token(request):
            return
    
        if not await validate_request(request, ['username', 'scammer_id', 'description']):
            return await bad_request(request, "'username', 'scammer_id' or 'description' is missing.")

        data = await request.json()

        if await has_reported(request.discordid, data['scammer_id']):
            return await conflict(request, 'You have already reported this user')

        await add_report(
            data['username'], data['scammer_id'], data['description'],
            request.discordid, request.client_ip
        )
        reports_count = await get_total_reports_for_scammer(data['scammer_id'])
        return await success(request, 'Report submitted successfully', {'reports_count': reports_count})
    except Exception as error:
        return json({"error": f"Something bad happened: {error}"}, status=500)
    
def register_reporting_routes(app: Application) -> None:
    app.router.add_post("/api/v1/reporting/report-user", report_user)
