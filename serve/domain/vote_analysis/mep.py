from pydantic import BaseModel


class MEP(BaseModel):
    name: str
    current_group_short_name: str
