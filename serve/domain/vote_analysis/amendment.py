
import re
from abc import abstractmethod
from typing import List

from pydantic import BaseModel

from serve.domain.vote_analysis.minutes import Minutes
from serve.domain.vote_analysis.page import Page


class Amendment(BaseModel):
    id: str
    minutes_id: str
    pages: List[Page]

    def _get_str_amendment_votes(self) -> str:
        # get amendment full text
        full_text = "\n".join([page.text for page in sorted(self.pages)])
        # keep the original votes only and discard potential correction votes
        correction_regex = r'ПОПРАВКИ[\S\s]+RÖSTER'
        original_votes = re.split(correction_regex, full_text)[0]
        return original_votes


class Amendments(BaseModel):

    @abstractmethod
    def save_amendments(self, minutes: Minutes, amendment_ids: List[str]):
        raise NotImplementedError
