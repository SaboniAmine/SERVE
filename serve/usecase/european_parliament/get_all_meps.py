from typing import List

from serve.domain.european_parliament.mep import (MEP, MEPs)


class GetAllMepsUsecase:
    def __init__(self, meps_repository: MEPs):
        self.meps_repository = meps_repository

    def get_all_meps(self) -> List[MEP]:
        return self.meps_repository.get_all_meps()
