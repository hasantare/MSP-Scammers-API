from typing import Dict, Any
import json

class ResponseBuilder:
    def __init__(self, status_code: int):
        self.status_code = status_code
        self.data = {}

    def set_success(self, data: Dict[str, Any]):
        self.data = data
        return self

    def set_error(self, message: str):
        self.data = {"error": message}
        return self

    def build(self):
        return json(self.data, status=self.status_code)

async def bad_request(message):
    return ResponseBuilder(400).set_error(message).build()

async def conflict(message):
    return ResponseBuilder(409).set_error(message).build()

async def success(data):
    return ResponseBuilder(200).set_success(data).build()