import uuid
from contextlib import AbstractContextManager

from dependency_injector.providers import Callable
from typing import List

from serve.domain.vote_analysis.vote import NormalizedVote, Votes
from serve.infra.database import sql_model
from serve.logger import logger
from sqlalchemy import select

class VotesSqlRepository(Votes):

    def __init__(
            self,
            session_factory: Callable,
    ) -> Callable[..., AbstractContextManager]:
        self.session_factory = session_factory

    def save_votes(self, votes: List[NormalizedVote]):
        with self.session_factory() as session:
            votes_sql_objects = [self.map_vote_to_sql(vote) for vote in votes]
            session.add_all(votes_sql_objects)
            session.commit()
            logger.info(
                f"{len(votes)} vote have been saved in base.",
            )

    def map_vote_to_sql(self, vote: NormalizedVote) -> sql_model.Votes:
        return sql_model.Votes(
            votes_id=uuid.uuid4(),
            mep_id=self.get_mep_id_from_full_name(vote.mep.full_name),
            value=vote.value,
            amendment_id=self.get_amendment_id_from_label(vote.amendment_id),
            group_id_at_vote=vote.group_id_at_vote.value
        )

    def get_mep_id_from_full_name(self, name: str):
        with self.session_factory() as session:
            return session.execute(
                select(sql_model.MEP.mep_id).where(sql_model.MEP.full_name == name)
            ).all()[0][0]

    def get_amendment_id_from_label(self, label: str):
        with self.session_factory() as session:
            return session.execute(
                select(sql_model.Amendments.amendment_id).where(sql_model.Amendments.label == label)
            ).all()[0][0]
