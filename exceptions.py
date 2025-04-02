class InvalidInputError(Exception):
    def __init__(self, msg: str):
        super().__init__(f"Invalid input. {msg}")
