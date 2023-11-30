from abc import abstractmethod
from enum import Enum
from typing import List

from pydantic import BaseModel

from serve.domain.european_parliament.european_parliament import \
    EuropeanParliamentMEP


class GroupsEnum(Enum):
    ECR = "ECR"
    GUE_NGL = "GUE/NGL"
    ID = "ID"
    NI = "NI"
    PPE = "PPE"
    Renew = "Renew"
    SD = "S&D"
    Verts = "Verts/ALE"

    @classmethod
    def _missing_(cls, value):
        return cls.NI


class Groups(BaseModel):
    group_short_name: GroupsEnum
    group_full_name: str


class MEP(BaseModel):
    id: int
    full_name: str
    current_group_short_name: GroupsEnum
    country: str
    is_active: bool


class MEPs(BaseModel):

    @abstractmethod
    def get_by_id(self, mep_id: int) -> MEP:
        raise NotImplemented

    @abstractmethod
    def get_all_meps(self) -> List[MEP]:
        raise NotImplemented

    @abstractmethod
    def update_group(self, mep_id: int, new_group: GroupsEnum) -> MEP:
        raise NotImplemented

    @abstractmethod
    def update_activity_status(self, mep_id: int, activity_status: bool) -> MEP:
        raise NotImplemented

    @abstractmethod
    def create_from_official_source(self, mep: EuropeanParliamentMEP) -> MEP:
        raise NotImplemented

    @abstractmethod
    def create_batch_from_official_source(self, meps: List[EuropeanParliamentMEP]) -> int:
        raise NotImplemented
