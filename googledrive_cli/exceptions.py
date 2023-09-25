class UserNotExistsError(Exception):
    def __init__(self):
        super().__init__("Incorrect login information")
