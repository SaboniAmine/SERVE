from typing import List

from serve.domain.european_parliament.mep import (EuropeanParliamentMEP,
                                                  EuropeanParliamentMEPSource,
                                                  MEPs)


class CreateAllMepsUsecase:
    def __init__(self,
                 meps_repository: MEPs,
                 meps_official_source: EuropeanParliamentMEPSource
                 ):
        self.meps_repository = meps_repository
        self.meps_official_source = meps_official_source

    def load_all_meps(self) -> int:
        meps_from_official_source: List[EuropeanParliamentMEP] = self.meps_official_source.get_updated_list()
        outgoing_meps_from_official_source: List[EuropeanParliamentMEP] = self.meps_official_source.get_outgoing_list()
        self.meps_repository.create_all_groups()
        return self.meps_repository.create_batch_from_official_source(meps_from_official_source + outgoing_meps_from_official_source)
