from typing import Optional, Any


class ClientException(Exception):

    def __init__(
            self,
            message: Optional[str] = "An unknown error occurred",
            status_code: Optional[int] = 400,
            success: Optional[bool] = False,
            data: Optional[Any] = None
    ):
        self.message = message
        self.status_code = status_code
        self.success = success
        self.data = data


class ServerException(Exception):

    def __init__(
            self,
            message: Optional[str] = "Server error",
            status_code: Optional[int] = 400,
            success: Optional[bool] = False,
            data: Optional[Any] = None
    ):
        self.message = message
        self.status_code = status_code
        self.success = success
        self.data = data
