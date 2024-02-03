import uuid
from contextlib import AbstractContextManager
from datetime import datetime
from typing import List

from dependency_injector.providers import Callable

from serve.domain.vote_analysis.minutes import Amendments, Minutes
from serve.infra.database import sql_model
from serve.logger import logger


class AmendmentsSqlRepository(Amendments):
    def __init__(
            self,
            session_factory: Callable,
    ) -> Callable[..., AbstractContextManager]:
        self.session_factory = session_factory

    def save_amendments(self, minutes: Minutes, amendment_ids: List[str]):
        with self.session_factory() as session:
            amendments_sql_objects = [self.map_amendment_to_sql(minutes, amendment_id) for amendment_id in amendment_ids]
            session.add_all(amendments_sql_objects)
            session.commit()
            logger.info(
                f"{len(amendment_ids)} amendments have been saved in base.",
            )

    def map_amendment_to_sql(self, minutes: Minutes, amendment_id: str) -> sql_model.Votes:
        amendments_matched = [x for x in minutes.amendments_list if x.id == amendment_id]
        if len(amendments_matched) == 0:
            raise ValueError(f"No amendment found with id {amendment_id}.")
        amendment = amendments_matched[0]
        amendment_first_page = min(amendment.pages)
        return sql_model.Amendments(
            amendment_id=uuid.uuid4(),
            type=minutes.type,
            binding_value=minutes.binding_value,
            url=minutes.id,
            label=amendment_id,
            date=datetime.strptime(minutes.date, "%d/%m/%Y"),
            page_number=amendment_first_page.id
        )
