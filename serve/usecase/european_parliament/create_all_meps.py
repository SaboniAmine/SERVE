from typing import List

from serve.domain.european_parliament.mep import EuropeanParliamentMEP, EuropeanParliamentMEPSource
from serve.domain.european_parliament.mep import MEPs


class CreateAllMepsUsecase:
    def __init__(self,
                 meps_repository: MEPs,
                 meps_official_source: EuropeanParliamentMEPSource
                 ):
        self.meps_repository = meps_repository
        self.meps_official_source = meps_official_source

    def load_all_meps(self) -> int:
        meps_from_official_source: List[EuropeanParliamentMEP] = self.meps_official_source.get_updated_list()
        return self.meps_repository.create_batch_from_official_source(meps_from_official_source)

