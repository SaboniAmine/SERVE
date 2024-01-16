from dataclasses import dataclass


@dataclass
class ErrorBase:
    message: str
