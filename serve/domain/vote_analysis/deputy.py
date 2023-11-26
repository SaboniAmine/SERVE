from pydantic import BaseModel


class Deputy(BaseModel):
    id: str
    name: str
    actual_group: str
    group_at_time: str
