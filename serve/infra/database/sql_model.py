from sqlalchemy import Integer, String, Column, Boolean, UUID, TIMESTAMP

from serve.infra.database.database_manager import Base


class MEP(Base):
    __tablename__ = "meps"
    mep_id = Column("mep_id", Integer, primary_key=True, index=True)
    full_name = Column("full_name", String)
    current_group_id = Column(String)
    country = Column(String)
    is_active = Column(Boolean)


class Groups(Base):
    __tablename__ = "groups"
    group_id = Column("group_id", String, primary_key=True, index=True)
    group_full_name = Column("group_full_name", String)


class Amendments(Base):
    __tablename__ = "amendments"
    amendment_id = Column("amendment_id", UUID, primary_key=True, index=True)
    type = Column("type", String)
    url = Column("url", String)
    label = Column("label", String)
    binding_value = Column("binding_value", Integer)
    date = Column("date", TIMESTAMP)
    page_number = Column("page_number", Integer)


class Votes(Base):
    __tablename__ = "votes"
    votes_id = Column("votes_id", UUID, primary_key=True, index=True)
    mep_id = Column("mep_id", Integer)
    value = Column("value", String)
    amendment_id = Column("amendment_id", String)
    group_id_at_vote = Column("group_id_at_vote", String)


class Events(Base):
    __tablename__ = "events"
    mep_events = Column("votes_id", UUID, primary_key=True, index=True)
    value = Column("value", Integer)
    resolution_id = Column("resolution_id", String)
    group_id_at_vote = Column("group_id_at_vote", String)
