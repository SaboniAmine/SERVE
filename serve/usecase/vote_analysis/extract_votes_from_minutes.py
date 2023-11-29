from typing import Any, List

from serve.domain.vote_analysis.amendment import Amendments
from serve.domain.vote_analysis.minutes import MinutesAggregate
from serve.domain.vote_analysis.vote import Votes


class ExtractVotesFromMinutesUsecase:
    def __init__(self,
                 votes_repository: Votes,
                 amendments_repository: Amendments
                 ):
        self.votes_repository = votes_repository
        self.amendments_repository = amendments_repository

    def read_minutes_and_extract_votes(self, minutes_pdf: Any, amendment_ids: List[str]):
        minutes = self.convert_minutes_from_pdf(minutes_pdf)
        votes = MinutesAggregate.extract_votes_from_amendments(minutes, amendment_ids)
        self.amendments_repository.save_amendments(minutes, amendment_ids)
        self.votes_repository.save_votes(votes)

    @staticmethod
    def convert_minutes_from_pdf(minutes_pdf: Any):
        pass
