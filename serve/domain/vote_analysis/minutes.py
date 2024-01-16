import re
from abc import abstractmethod
from typing import Dict, List, Optional

from pydantic import BaseModel, model_validator

from serve.domain.vote_analysis.mep import MEPReadFromMinutes
from serve.domain.vote_analysis.page import Page
from serve.domain.vote_analysis.vote import Vote
from serve.logger import logger


class Amendment(BaseModel):
    id: str
    minutes_id: str
    pages: List[Page]

    def get_str_amendment_votes(self) -> str:
        # get amendment full text
        full_text = "\n".join([page.text for page in sorted(self.pages)])
        # keep the original votes only and discard potential correction votes
        correction_regex = r'\nПОПРАВКИ[\S\s]+RÖSTER'
        original_votes = re.split(correction_regex, full_text)[0]
        return original_votes


class Minutes(BaseModel):
    id: str
    type: Optional[str]
    pages_list: List[Page]
    date: str = None
    amendments_list: List[Amendment] = []

    def _get_amendment_infos_from_body(self) -> Dict:
        # read for every amendment its name, id in the document and first page number
        amendment_infos = {}
        previous_amendment_name = None
        for page in sorted(self.pages_list):
            if page.header is not None:
                amendment_name = page.extract_amendment_name_from_header()
                amendment_infos[amendment_name] = [page]
                previous_amendment_name = amendment_name
            elif previous_amendment_name is not None:
                amendment_infos[amendment_name].append(page)
        return amendment_infos

    @model_validator(mode="after")
    def extract_amendments(self) -> "Minutes":
        amendment_infos = self._get_amendment_infos_from_body()
        for amendment_name, pages in amendment_infos.items():
            self.amendments_list.append(
                Amendment(id=amendment_name, minutes_id=self.id, pages=pages)
            )
        return self

    @model_validator(mode="after")
    def extract_date(self) -> "Minutes":
        date_regex = r"\d{1,2}/\d{1,2}/\d{4}"
        date_first_page = re.findall(date_regex, self.pages_list[0].text)
        date_second_page = re.findall(date_regex, self.pages_list[1].text)  # handle exceptional cases
        if len(date_first_page) != 0:
            self.date = date_first_page[0]
        elif len(date_second_page) != 0:
            self.date = date_second_page[0]
        return self

    def __hash__(self) -> int:
        return hash((type(self), self.id, self.type, self.date))

class MinutesAggregate:

    @staticmethod
    def extract_votes_from_amendments(minutes: Minutes, amendment_ids: List[str]) -> List[Vote]:
        amendments = [x for x in minutes.amendments_list if x.id in amendment_ids]
        votes = []
        for amendment in amendments:
            original_votes = amendment.get_str_amendment_votes()
            # split vote by category (for, against, null)
            regex_vote_categories = r"(\d+)([+0-])"
            votes_by_category = re.split(regex_vote_categories, original_votes)[1:]

            # for every vote category, extract the deputies
            regex_group = r"\n+?(.+?): *"
            for i in range(0, len(votes_by_category), 3):
                expected_category_total_votes = int(votes_by_category[i])
                vote_category = votes_by_category[i + 1]
                votes_bucket = votes_by_category[i + 2]
                votes_by_group = re.split(regex_group, votes_bucket)
                extracted_category_votes = 0
                for i in range(1, len(votes_by_group), 2):
                    group_name = votes_by_group[i]
                    group_voters = votes_by_group[i + 1].replace('\n', '').split(', ')
                    for name in group_voters:
                        mep = MEPReadFromMinutes(
                            name=name,
                            current_group_short_name=group_name
                        )
                        votes.append(Vote(amendment_id=amendment.id, value=vote_category, mep=mep))
                        extracted_category_votes += 1
                try:
                    assert expected_category_total_votes == extracted_category_votes  # transformer exception métier
                except AssertionError:
                    logger.warning(f'Delta between expected number of votes ({expected_category_total_votes}) and extracted number of votes ({extracted_category_votes}).')
        return votes


class Amendments:

    @abstractmethod
    def save_amendments(self, minutes: Minutes, amendment_ids: List[str]):
        raise NotImplementedError