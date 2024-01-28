from typing import List

from serve.domain.european_parliament.mep import MEPs
from serve.domain.vote_analysis.vote import NormalizedVote


class GetMEPVotesUsecase:
    def __init__(self, meps_repository: MEPs):
        self.meps_repository = meps_repository

    def get_mep_votes(self, mep_id: int) -> List[NormalizedVote]:
        return self.meps_repository.get_all_votes(mep_id)
