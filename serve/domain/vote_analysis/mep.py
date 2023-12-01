from pydantic import BaseModel

from serve.domain.european_parliament.mep import GroupsEnum


class MEPReadFromMinutes(BaseModel):
    name: str
    current_group_short_name: GroupsEnum


class NormalizedMEP(BaseModel):
    id: int
    full_name: str
    current_group_short_name: GroupsEnum
