from typing import List, Optional

from serve.logger import logger
from serve.domain.european_parliament.european_parliament import EuropeanParliamentMEP, EuropeanParliamentMEPSource
from serve.domain.european_parliament.mep import MEPs, MEP, GroupsEnum
from serve.infra.database import sql_model


class MepsSqlRepository(MEPs):

    def get_by_id(self, mep_id: int) -> Optional[MEP]:
        with self.session_factory() as session:
            mep = session.query(sql_model.MEP).filter(
                sql_model.MEP.mep_id == mep_id
            )
        if mep:
            return self.map_sql_mep_to_mep(mep)

    def get_all_meps(self) -> List[MEP]:
        with self.session_factory() as session:
            meps = session.query(sql_model.MEP)
        if not meps:
            return []
        return [self.map_sql_vessel_to_schema(mep) for mep in meps]

    def update_group(self, mep_id: int, new_group: GroupsEnum) -> MEP:
        pass

    def update_activity_status(self, mep_id: int, activity_status: bool) -> MEP:
        pass

    def create_from_official_source(self, mep: EuropeanParliamentMEP):
        with self.session_factory() as session:
            session.add(self.map_european_parliament_mep_to_sql(mep))
            session.commit()
            logger.info(
                f"{mep} mep have been saved in base.",
            )

    def create_batch_from_official_source(self, meps: List[EuropeanParliamentMEP]) -> int:
        with self.session_factory() as session:
            meps_sql_objects = [self.map_european_parliament_mep_to_sql(mep) for mep in meps]
            session.add_all(meps_sql_objects)
            session.commit()
            logger.info(
                f"{len(meps_sql_objects)} meps have been saved in base.",
            )
        return len(meps_sql_objects)

    @staticmethod
    def map_european_parliament_mep_to_sql(mep: EuropeanParliamentMEP) -> sql_model.MEP:
        return sql_model.MEP(
            id=mep.id,
            full_name=mep.full_name,
            current_group_id=EuropeanParliamentMEPSource.group_full_name_to_short_political_group(mep.group_full_name),
            country=mep.country,
            is_active=True
        )

    @staticmethod
    def map_sql_mep_to_mep(sql_mep: sql_model.MEP) -> MEP:
        return MEP(
            id=sql_mep.mep_id,
            full_name=sql_mep.full_name,
            current_group_short_name=GroupsEnum(sql_mep.current_group_id),
            country=sql_mep.country,
            is_active=sql_mep.is_active
        )
