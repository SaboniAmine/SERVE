import re
from typing import Dict, List

from pydantic import BaseModel, model_validator

from serve.domain.vote_analysis.amendment import Amendment
from serve.domain.vote_analysis.mep import MEP
from serve.domain.vote_analysis.page import Page
from serve.domain.vote_analysis.vote import Vote


def get_mep_full_name_and_group(name: str, group_name: str):
    """ TO IMPLEMENT"""
    return name, group_name


class Minutes(BaseModel):
    id: str
    pages_list: List[Page]
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

class MinutesAggregate(BaseModel):

    def extract_votes_from_amendments(minutes: Minutes, amendment_ids: List[str]) -> List[Vote]:
        amendments = [x for x in minutes.amendments_list if x.id in amendment_ids]
        votes = []
        for amendment in amendments:
            original_votes = amendment._get_str_amendment_votes()
            # split vote by category (for, against, null)
            regex_vote_categories = r"(\d+)([+0-])"
            votes_by_category = re.split(regex_vote_categories, original_votes)[1:]

            # for every vote category, extract the deputies
            regex_group = r"\n+?(.+?): *"
            for i in range(0, len(votes_by_category), 3):
                expected_category_total_votes = int(votes_by_category[i])
                vote_category = votes_by_category[i + 1]
                votes = votes_by_category[i + 2]
                votes_by_group = re.split(regex_group, votes)
                extracted_category_votes = 0
                for i in range(1, len(votes_by_group), 2):
                    group_name = votes_by_group[i]
                    group_voters = votes_by_group[i + 1].replace('\n', '').split(', ')
                    for name in group_voters:
                        name, current_group_short_name = get_mep_full_name_and_group(name, group_name)
                        mep = MEP(
                            name=name,
                            current_group_short_name=current_group_short_name
                        )
                        votes.append(Vote(amendment_id=amendment.id, value=vote_category, mep=mep))
                        extracted_category_votes += 1
                assert expected_category_total_votes == extracted_category_votes  # transformer exception métier
        return votes
