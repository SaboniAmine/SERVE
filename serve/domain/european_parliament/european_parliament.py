from abc import abstractmethod
from typing import List

from pydantic import BaseModel

from serve.domain.european_parliament.mep import GroupsEnum


class EuropeanParliamentMEP(BaseModel):
    id: int
    full_name: str
    country: str
    group_full_name: str
    national_political_group: str


class EuropeanParliamentMEPSource(BaseModel):
    long_to_short_group = {
        "Group of the European People's Party (Christian Democrats)": GroupsEnum.PPE,
        "Identity and Democracy Group": GroupsEnum.ID,
        "Group of the Progressive Alliance of Socialists and Democrats in the European Parliament": GroupsEnum.SD,
        "European Conservatives and Reformists Group": GroupsEnum.ECR,
        "Group of the Greens/European Free Alliance": GroupsEnum.Verts,
        "Renew Europe Group": GroupsEnum.Renew,
        "The Left group in the European Parliament - GUE/NGL": GroupsEnum.GUE_NGL,
        "Non-attached Members": GroupsEnum.NI,
    }

    @abstractmethod
    def get_updated_list(self) -> List[EuropeanParliamentMEP]:
        raise NotImplemented

    @classmethod
    def group_full_name_to_short_political_group(cls, group_full_name: str) -> GroupsEnum:
        return cls.long_to_short_group[group_full_name]
