from db import fetchone
from googledrive_cli.response import *


class Authenticator:

    def __init__(self):
        pass

    def authenticate(self, email: str, password: str) -> str:
        # Logic of authentication; return status
        user_data = fetchone("SELECT * FROM user WHERE email=?, password=?", (email, password))
        if not user_data:
            return RESPONSE_MESSAGE_ERROR
        return RESPONSE_MESSAGE_SUCCESS


