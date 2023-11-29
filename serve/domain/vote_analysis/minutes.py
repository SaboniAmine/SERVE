import re
from typing import Dict, List

from pydantic import BaseModel, model_validator

from .deputy import Deputy
from .vote import Vote


def get_deputy_full_name_and_group(name: str, group_name: str):
    """ TO IMPLEMENT"""
    return name, group_name

class Page(BaseModel):
    id: int
    text: str
    header: str = None
    footer: str = None

    def _build_footer_regex(self) -> str:
        regex_footer = r"^.*\d{3}\.\d{3}"
        found_footer = re.findall(regex_footer, self.text)
        if len(found_footer) != 1:
            raise Exception(f"Error extracting footer, should have exactly one match but got {len(found_footer)}")
        splited_footer = found_footer[0].split()
        footer_regex = re.escape(splited_footer[0]) + r"\s\d+.*?" + re.escape(splited_footer[-1])
        return footer_regex

    @model_validator(mode="after")
    def extract_footer(self) -> "Page":
        if self.footer is None:
            footer_regex = self._build_footer_regex()
            footer_found = re.findall(footer_regex, self.text)
            if len(footer_found) == 1:
                self.footer = footer_found[0]
                self.text = re.split(footer_regex, self.text)[1]
            elif len(footer_found) > 1:
                raise Exception('Error extracting footer, found multiple match.')
        return self

    @model_validator(mode="after")
    def extract_header(self) -> "Page":
        if self.header is None:
            header_regex = r"^\d+\.\s.+\s\d{1,2}/\d{1,2}/\d{4}\s\d{2}:\d{2}:\d{2}.\d{3}\n"
            header_found = re.findall(header_regex, self.text)
            if len(header_found) == 1:
                self.header = header_found[0]
                self.text = re.split(header_regex, self.text)[1]
            elif len(header_found) > 1:
                raise Exception('Error extracting header, found multiple match.')
        return self

    def __lt__(self, other: "Page"):
        return self.id < other.id

    def extract_amendment_name_from_header(self):
        if self.header is None:
            return None
        extract_regex = r"^\d+\.\s(.+)\s\d{1,2}/\d{1,2}/\d{4}\s\d{2}:\d{2}:\d{2}.\d{3}\n"
        amendment_name = re.findall(extract_regex, self.header)[0]
        return amendment_name


class Amendment(BaseModel):
    id: str
    minutes_id: str
    pages: List[Page]
    votes: List[Vote] = []

    @model_validator(mode='after')
    def extract_votes(self) -> "Amendment":
        if len(self.pages) == 0:
            raise ValueError('Empty list of pages')
        original_votes = self._get_str_amendment_votes()
        # split vote by category (for, against, null)
        regex_vote_categories = r"(\d+)([+0-])"
        votes_by_category = re.split(regex_vote_categories, original_votes)[1:]

        # for every vote category, extract the deputies
        self.votes = []
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
                    full_name, actual_group = get_deputy_full_name_and_group(name, group_name)
                    deputy = Deputy(
                        id=full_name,
                        name=full_name,
                        actual_group=actual_group,
                        group_at_time=group_name
                    )
                    self.votes.append(Vote(amendment_id=self.id, value=vote_category, deputy=deputy))
                    extracted_category_votes += 1
            assert expected_category_total_votes == extracted_category_votes
        return self

    def _get_str_amendment_votes(self) -> str:
        # get amendment full text
        full_text = "\n".join([page.text for page in sorted(self.pages)])
        # keep the original votes only and discard potential correction votes
        correction_regex = r'ПОПРАВКИ[\S\s]+RÖSTER'
        original_votes = re.split(correction_regex, full_text)[0]
        return original_votes


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
