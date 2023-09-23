from googledrive_cli.naming_service import NamingService


class Requestor:
    def __init__(self):
        pass

    def login(self, email: str, password: str, jwt_token: str):
        response = NamingService.authenticator.authenticate(email, password, jwt_token)
        pass







