from abc import abstractmethod
from typing import List

from pydantic import BaseModel
from typing_extensions import Literal

from serve.domain.vote_analysis.mep import MEP


class Vote(BaseModel):
    amendment_id: str
    mep: MEP
    value: Literal['+', '-', '0']

class Votes(BaseModel):

    @abstractmethod
    def save_votes(votes: List[Vote]):
        raise NotImplementedError
