from dataclasses import dataclass


@dataclass
class ErrorBase:
    message: str


class NotFoundError(ErrorBase):
    pass


class NotFoundException(Exception):
    def __init__(self, error: NotFoundError) -> None:
        self.error = error
