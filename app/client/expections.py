

class AppError(Exception):
    pass


class ClientError(AppError):
    "Base Exeption class using for Client API errors"
    def __init__(self, api_name, msg):
        self.api_name = api_name
        self.msg = msg
        super().__init__(f"{api_name}: {msg}")


class ClientAPIError(ClientError):
    "Raises when some error with API requests has occurred"
    pass


class ClientInternalError(ClientError):
    """
    Raises when something has happened inside the app logic
    (for example, cannot get some value by key)
    """
    pass


class BreakingRequestLimitError(ClientError):
    """
    Raises when request limit has been broken or IP adress is banned
    """
    pass

class DialectParsingError(AppError):
    """Raises during dialect parsing"""
    pass
