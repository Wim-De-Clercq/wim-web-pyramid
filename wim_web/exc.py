
class DatabaseResourceNotFound(Exception):

    def __init__(self, msg:str) -> None:
        super().__init__(msg)
        self.msg = msg
        self.message = msg
