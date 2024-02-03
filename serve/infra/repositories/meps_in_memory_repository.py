from typing import List

from serve.domain.european_parliament.mep import (MEP, EuropeanParliamentMEP,
                                                  GroupsEnum, MEPs)
from serve.domain.vote_analysis.vote import Vote


class MepsInMemoryRepository(MEPs):
    def __init__(self):
        super().__init__()
        self.meps = [MEP(
            id="1",
            full_name="John DOE",
            current_group_short_name=GroupsEnum.NI,
            country="France",
            is_active=True
        ), MEP(
            id="2",
            full_name="Franck ALUMNI",
            current_group_short_name=GroupsEnum.PPE,
            country="Germany",
            is_active=True
        ), MEP(
            id="3",
            full_name="Gontran BONHEUR",
            current_group_short_name=GroupsEnum.Renew,
            country="Spain",
            is_active=False
        )]

    def get_by_id(self, mep_id: int) -> MEP:
        return list(filter(lambda x: x.minutes_id == mep_id, self.meps))[0]

    def get_all_meps(self) -> List[MEP]:
        return self.meps

    def update_group(self, mep_id: int, new_group: GroupsEnum) -> MEP:
        pass

    def get_all_votes(self, mep_id: int) -> List[Vote]:
        pass

    def update_activity_status(self, mep_id: int, activity_status: bool) -> MEP:
        pass

    def create_from_official_source(self, mep: EuropeanParliamentMEP) -> MEP:
        pass

    def create_batch_from_official_source(self, meps: List[EuropeanParliamentMEP]) -> int:
        pass
