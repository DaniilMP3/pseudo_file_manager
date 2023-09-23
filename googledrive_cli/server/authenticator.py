from typing import Literal


class JWTGenerator:
    def __init__(self):
        pass

    @staticmethod
    def generate_jwt_token():
        pass


class Authenticator:
    RESPONSE_MESSAGE_SUCCESS = 'OK'
    RESPONSE_MESSAGE_ERROR = 'ERR'

    _jwt_generator = JWTGenerator()

    def __init__(self):
        pass

    def authenticate(self, email: str, password: str, jwt_token: str) -> str:
        # Logic of authentication; return status

        pass
