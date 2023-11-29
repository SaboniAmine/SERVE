from pydantic import BaseModel
from typing_extensions import Literal

from .deputy import Deputy


class Vote(BaseModel):
    amendment_id: str
    value: Literal['+', '-', '0']
    deputy: Deputy
