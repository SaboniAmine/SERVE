from dataclasses import dataclass
from enum import Enum

from serve.errors import ErrorBase


class MinutesParsingErrorEnum(Enum):
    HEADER_ERROR = "HEADER_ERROR"
    HEADER_NOT_FOUND = "HEADER_NOT_FOUND"
    MULTIPLE_HEADERS_FOUND = "MULTIPLE_HEADERS_FOUND"
    FOOTER_ERROR = "FOOTER_ERROR"
    FOOTER_NOT_FOUND = "FOOTER_NOT_FOUND"
    MULTIPLE_FOOTERS_FOUND = "MULTIPLE_FOOTERS_FOUND"
    PROGRAMMING_ERROR = "PROGRAMMING_ERROR"


@dataclass(kw_only=True)
class MinutesParsingError(ErrorBase):
    code: MinutesParsingErrorEnum


class MinutesParsingException(Exception):
    def __init__(self, error: MinutesParsingError) -> None:
        self.error = error
