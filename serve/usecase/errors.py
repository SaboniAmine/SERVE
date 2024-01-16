from serve.errors import ErrorBase


class NotFoundError(ErrorBase):
    pass


class NotFoundException(Exception):
    def __init__(self, error: NotFoundError) -> None:
        self.error = error
