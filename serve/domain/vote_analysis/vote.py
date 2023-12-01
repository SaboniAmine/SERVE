from abc import abstractmethod
from typing import List

from pydantic import BaseModel
from typing_extensions import Literal

from serve.domain.european_parliament.mep import MEP, GroupsEnum
from serve.domain.vote_analysis.mep import MEPReadFromMinutes


class Vote(BaseModel):
    amendment_id: str
    mep: MEPReadFromMinutes
    value: Literal['+', '-', '0']


class NormalizedVote(Vote):
    mep: MEP
    group_id_at_vote: GroupsEnum


class Votes:

    @abstractmethod
    def save_votes(self, votes: List[Vote]):
        raise NotImplementedError
