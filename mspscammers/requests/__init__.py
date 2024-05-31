from typing import Awaitable, Tuple, Optional

class RequestValidator:
    def __init__(self, request: Awaitable, required_fields: Tuple[str,...]):
        self.request = request
        self.required_fields = required_fields

    async def validate(self) -> Tuple[bool, Optional[str]]:
        data = await self.request.json()
        for field in self.required_fields:
            if not data.get(field):
                return False, f"Missing or empty field: {field}"
        return True, None
