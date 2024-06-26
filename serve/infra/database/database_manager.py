from collections.abc import Callable
from contextlib import AbstractContextManager, contextmanager

from sqlalchemy import create_engine, exc, orm
from sqlalchemy.orm import Session, declarative_base

from serve.infra.database.errors import DBError, DBErrorEnum, DBException
from serve.logger import logger

Base = declarative_base()


class Database:
    def __init__(self, db_url: str) -> None:
        self._engine = create_engine(db_url)
        self._session_factory = orm.scoped_session(
            orm.sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self._engine,
            ),
        )

    def create_database(self) -> None:
        Base.metadata.create_all(self._engine)

    @contextmanager
    def session(self) -> Callable[..., AbstractContextManager]:
        session: Session = self._session_factory()
        try:
            yield session

        except exc.IntegrityError as e:
            session.rollback()
            logger.exception(e.orig.args[0], exc_info=True)
            raise DBException(
                error=DBError(
                    code=DBErrorEnum.INTEGRITY_ERROR,
                    message="Relation not found, or duplicate key",
                ),
            ) from e
        except exc.DataError as e:
            session.rollback()
            logger.exception(e.orig.args[0], exc_info=True)
            raise DBException(
                error=DBError(code=DBErrorEnum.DATA_ERROR, message="Invalid data"),
            ) from e
        except exc.ProgrammingError as e:
            session.rollback()
            logger.exception(e.orig.args[0], exc_info=True)
            raise DBException(
                error=DBError(
                    code=DBErrorEnum.PROGRAMMING_ERROR,
                    message="Wrong schema",
                ),
            ) from e
        except Exception:
            logger.exception("Session rollback because of exception", exc_info=True)
            session.rollback()
            raise
        finally:
            session.close()
