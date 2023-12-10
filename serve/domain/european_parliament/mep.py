from abc import abstractmethod
from enum import Enum
from typing import List, Dict

from pydantic import BaseModel


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


class EuropeanParliamentMEP(BaseModel):
    id: int
    full_name: str
    country: str
    group_full_name: str
    national_political_group: str
    is_active: bool


class MEPs:

    @abstractmethod
    def get_by_id(self, mep_id: int) -> MEP:
        raise NotImplemented

    @abstractmethod
    def get_all_meps(self) -> List[MEP]:
        raise NotImplemented

    @abstractmethod
    def create_all_groups(self):
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


class EuropeanParliamentMEPSource:
    long_to_short_group: Dict[str, GroupsEnum] = {
        "Group of the European People's Party (Christian Democrats)": GroupsEnum.PPE,
        "Identity and Democracy Group": GroupsEnum.ID,
        "Group of the Progressive Alliance of Socialists and Democrats in the European Parliament": GroupsEnum.SD,
        "European Conservatives and Reformists Group": GroupsEnum.ECR,
        "Group of the Greens/European Free Alliance": GroupsEnum.Verts,
        "Renew Europe Group": GroupsEnum.Renew,
        "The Left group in the European Parliament - GUE/NGL": GroupsEnum.GUE_NGL,
        "Group of the European United Left - Nordic Green Left": GroupsEnum.GUE_NGL,
        "Non-attached Members": GroupsEnum.NI,
    }

    @abstractmethod
    def get_updated_list(self) -> List[EuropeanParliamentMEP]:
        raise NotImplemented

    @abstractmethod
    def get_outgoing_list(self) -> List[EuropeanParliamentMEP]:
        raise NotImplemented

    @classmethod
    def group_full_name_to_short_political_group(cls, group_full_name: str) -> GroupsEnum:
        return cls.long_to_short_group[group_full_name]
