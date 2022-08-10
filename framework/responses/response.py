import orjson
from typing import Any
from fastapi.responses import JSONResponse


class ClientResponse(JSONResponse):
    media_type = "application/json"

    def render(self, content: Any) -> bytes:
        assert orjson is not None, "orjson must be installed to use ORJSONResponse"
        success = True
        status_code = 200
        message = None
        data = content
        pagination = None
        if isinstance(content, dict) \
                and "success" in content and "status_code" in content and "message" in content and "data" in content:
            success = content["success"]
            status_code = content["status_code"]
            message = content["message"]
            data = content["data"]
            pagination = content.get("pagination")
        content = {
            "success": success,
            "status_code": status_code,
            "message": message,
            "data": data,
            "pagination": pagination
        }
        return orjson.dumps(content)
