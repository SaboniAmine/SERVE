from dataclasses import dataclass
from enum import Enum

from serve.errors import ErrorBase


class DBErrorEnum(Enum):
    INTEGRITY_ERROR = "INTEGRITY_ERROR"
    DATA_ERROR = "DATA_ERROR"
    PROGRAMMING_ERROR = "PROGRAMMING_ERROR"


@dataclass(kw_only=True)
class DBError(ErrorBase):
    code: DBErrorEnum


class DBException(Exception):
    def __init__(self, error: DBError) -> None:
        self.error = error
