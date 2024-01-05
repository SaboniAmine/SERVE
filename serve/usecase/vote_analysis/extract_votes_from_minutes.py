import regex as re
from typing import Any, List

from pypdf import PdfReader
from rapidfuzz.process import extractOne
from rapidfuzz.utils import default_process

from serve.domain.european_parliament.mep import MEPs, MEP
from serve.domain.vote_analysis.mep import MEPReadFromMinutes
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
        self.meps_processed_full_name = [default_process(mep.full_name) for mep in self.meps_list]
        # build preprocessed list of only name (not full name)
        regex_uppercase_name = r"([\p{Lu}][\p{Lu}\s]+)$"
        self.meps_processed_name = [
            default_process(re.findall(regex_uppercase_name, mep.full_name)[0])
            for mep in self.meps_list
        ]

    def read_minutes_and_extract_votes(
            self,
            minutes_id: str,
            minutes_type: str,
            minutes_pdf: Any,
            amendment_ids: List[str]
    ):
        minutes = self.convert_minutes_from_pdf(minutes_id, minutes_type, minutes_pdf)
        votes = MinutesAggregate.extract_votes_from_amendments(minutes, amendment_ids)
        normalized_votes = self.normalized_votes_read_from_minutes(votes)
        # raise Exception
        self.amendments_repository.save_amendments(minutes, amendment_ids)
        self.votes_repository.save_votes(normalized_votes)

    def normalized_votes_read_from_minutes(self, votes: List[Votes]) -> List[NormalizedVote]:
        normalized_votes = []
        for vote in votes:
            normalized_votes.append(
                NormalizedVote(
                    amendment_id=vote.amendment_id,
                    mep=self.build_mep_from_name(vote.mep, 95),
                    value=vote.value,
                    group_id_at_vote=vote.mep.current_group_short_name
                )
            )
        return normalized_votes

    def build_mep_from_name(self, mep: MEPReadFromMinutes, min_score: int) -> MEP:
        # Try to extract full name from current group, if sure enough we select its name
        same_group_mask = [x.current_group_short_name == mep.current_group_short_name for x in self.meps_list]
        # search only in the list of name, but if the name is composed, search in full names
        search_group = self.meps_processed_name
        if ' ' in mep.name:
            search_group = self.meps_processed_full_name
        fuzzy_search_results = extractOne(
            default_process(mep.name),
            [
                processed_full_name
                for processed_full_name, same_group in zip(search_group, same_group_mask)
                if same_group
            ],
            score_cutoff=min_score
        )
        if fuzzy_search_results is not None:
            return [mep for mep, same_group in zip(self.meps_list, same_group_mask) if same_group][fuzzy_search_results[2]]

        # If MEP cannot be found with its group, lets fuzzy search it in the MEPs list
        fuzzy_search_results = extractOne(
            default_process(mep.name),
            search_group,
            score_cutoff=min_score
        )
        if fuzzy_search_results is not None:
            return self.meps_list[fuzzy_search_results[2]]

        if min_score >= 60:
            return self.build_mep_from_name(mep, min_score - 1)
        logger.error(f"No MEP known with the name: {mep.name} in the database")
        raise NotFoundException(error=NotFoundError(f"No MEP known with the name: {mep.name} in the database"))

    @staticmethod
    def convert_minutes_from_pdf(minutes_id: str, minutes_type: str, minutes_pdf: Any):
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
            pages_list=page_list
        )
