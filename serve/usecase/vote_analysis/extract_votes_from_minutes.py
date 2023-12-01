from typing import Any, List

from PyPDF2 import PdfReader
from fuzzywuzzy import process

from serve.domain.european_parliament.mep import MEPs, MEP
from serve.domain.vote_analysis.minutes import MinutesAggregate, Amendments, Minutes
from serve.domain.vote_analysis.page import Page
from serve.domain.vote_analysis.vote import Votes, NormalizedVote
from serve.logger import logger
from serve.usecase.errors import NotFoundException, NotFoundError


class ExtractVotesFromMinutesUsecase:
    def __init__(self,
                 votes_repository: Votes,
                 meps_repository: MEPs,
                 amendments_repository: Amendments
                 ):
        self.votes_repository = votes_repository
        self.meps_repository = meps_repository
        self.amendments_repository = amendments_repository
        self.meps_list = meps_repository.get_all_meps()

    def read_minutes_and_extract_votes(
            self,
            minutes_id: str,
            minutes_type: str,
            minutes_pdf: Any,
            amendment_ids: List[str]
    ):
        minutes = self.convert_minutes_from_pdf(minutes_id, minutes_type, amendment_ids, minutes_pdf)
        votes = MinutesAggregate.extract_votes_from_amendments(minutes, amendment_ids)
        normalized_votes = self.normalized_votes_read_from_minutes(votes)
        # self.amendments_repository.save_amendments(minutes, amendment_ids)
        self.votes_repository.save_votes(normalized_votes)

    def normalized_votes_read_from_minutes(self, votes):
        normalized_votes = []
        for vote in votes:
            normalized_votes.append(
                NormalizedVote(
                    amendment_id=vote.amendment_id,
                    mep=self.build_mep_from_name(vote.mep),
                    value=vote.value,
                    group_id_at_vote=vote.mep.current_group_short_name
                )
            )
        return normalized_votes

    def build_mep_from_name(self, mep) -> MEP:
        # Try to extract full name from current group, if sure enough we
        fuzzy_search_results = process.extract(mep.name, list(map(lambda x: x.full_name, filter(
            lambda x: x.current_group_short_name == mep.current_group_short_name, self.meps_list))), limit=1)
        if fuzzy_search_results:
            probable_mep_name, probability = fuzzy_search_results[0]
            if probability > 85:
                full_name = probable_mep_name
                return list(filter(lambda x: x.full_name == full_name, self.meps_list))[0]
        # If MEP cannot be found with its group, lets fuzzy search it in the MEPs list
        try:
            fuzzy_search_results = process.extract(
                mep.name,
                list(map(lambda x: x.full_name, self.meps_list)), limit=1
            )[0]
            full_name, probability = fuzzy_search_results
            return list(filter(lambda x: x.full_name == full_name, self.meps_list))[0]
        except IndexError:
            logger.error(f"No MEP known with the name: {mep.name} in the database")
            raise NotFoundException(error=NotFoundError(f"No MEP known with the name: {mep.name} in the database"))

    @staticmethod
    def convert_minutes_from_pdf(minutes_id: str, minutes_type, amendments_list: List[str], minutes_pdf: Any):
        pdf = PdfReader(minutes_pdf)
        page_list = []
        for page_number, page in enumerate(pdf.pages):
            page_text = page.extract_text()
            page_list.append(
                Page(
                    id=page_number,
                    text=page_text
                )
            )
        return Minutes(
            id=minutes_id,
            type=minutes_type,
            pages_list=page_list,
            amendements_list=amendments_list
        )
