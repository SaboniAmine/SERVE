from contextlib import AbstractContextManager
from typing import List
from dependency_injector.providers import Callable

from serve.domain.vote_analysis.minutes import Minutes, Amendments


class AmendmentsSqlRepository(Amendments):
    def __init__(
            self,
            session_factory: Callable,
    ) -> Callable[..., AbstractContextManager]:
        self.session_factory = session_factory

    def save_amendments(self, minutes: Minutes, amendment_ids: List[str]):
        pass