import uuid
from contextlib import AbstractContextManager

from dependency_injector.providers import Callable
from typing import List

from serve.domain.vote_analysis.vote import Votes, Vote
from serve.infra.database import sql_model
from serve.logger import logger


class VotesSqlRepository(Votes):

    def __init__(
            self,
            session_factory: Callable,
    ) -> Callable[..., AbstractContextManager]:
        self.session_factory = session_factory

    def save_votes(self, votes: List[Vote]):
        with self.session_factory() as session:
            votes_sql_objects = [self.map_vote_to_sql(vote) for vote in votes]
            session.add_all(votes_sql_objects)
            session.commit()
            logger.info(
                f"{len(votes)} vote have been saved in base.",
            )

    def map_vote_to_sql(self, vote: Vote) -> sql_model.Votes:
        return sql_model.Votes(
            vote_id=uuid.uuid4(),
            mep_id=self.get_mep_id_from_partial_name(vote.mep.name),
            value=Vote.value,
        )
