from googledrive_cli.naming_service import NamingService
from googledrive_cli.response import *
from googledrive_cli.server.db import *
from googledrive_cli.exceptions import UserNotExistsError


class Requestor:
    def __init__(self):
        pass

    def login(self, email: str, password: str) -> bool:
        authenticator = NamingService.authenticator
        response = authenticator.authenticate(email, password)
        if response == RESPONSE_MESSAGE_SUCCESS:
            execute("UPDATE user SET is_authenticated = ? WHERE email = ? and password = ?", (1, email, password))
            return True
        else:
            raise UserNotExistsError()
