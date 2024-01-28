from dependency_injector import containers, providers

from serve.infra.database.database_manager import Database
from serve.infra.european_parliament_official_source import \
    XmlEuropeanParliamentMEPSource
from serve.infra.repositories.amendments_sql_repository import \
    AmendmentsSqlRepository
from serve.infra.repositories.meps_sql_repository import MepsSqlRepository
from serve.infra.repositories.votes_sql_repository import VotesSqlRepository
from serve.settings import settings
from serve.usecase.european_parliament.create_all_meps import \
    CreateAllMepsUsecase
from serve.usecase.european_parliament.get_all_meps import GetAllMepsUsecase
from serve.usecase.vote_analysis.extract_votes_from_minutes import \
    ExtractVotesFromMinutesUsecase
from serve.usecase.vote_analysis.get_mep_votes import GetMEPVotesUsecase
from serve.usecase.vote_analysis.initialize_votes_extract import \
    InitializeVotesExtractUsecase


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    db_url = settings.db_url
    mep_list_source = settings.mep_list_source
    outgoing_mep_list_source = settings.outgoing_mep_list_source
    db = providers.Singleton(
        Database,
        db_url=db_url,
    )

    votes_repository = providers.Factory(
        VotesSqlRepository,
        session_factory=db.provided.session,
    )

    amendments_repository = providers.Factory(
        AmendmentsSqlRepository,
        session_factory=db.provided.session,
    )

    meps_repository = providers.Factory(
        MepsSqlRepository,
        session_factory=db.provided.session,
    )

    meps_official_source = providers.Factory(
        XmlEuropeanParliamentMEPSource,
        mep_list_source=mep_list_source,
        outgoing_mep_list_source=outgoing_mep_list_source,
    )

    create_all_meps_usecase = providers.Factory(
        CreateAllMepsUsecase,
        meps_repository=meps_repository,
        meps_official_source=meps_official_source
    )

    initialize_votes_extract = providers.Factory(
        InitializeVotesExtractUsecase,
        votes_repository=votes_repository,
        meps_repository=meps_repository,
        amendments_repository=amendments_repository
    )

    extract_votes_usecase = providers.Factory(
        ExtractVotesFromMinutesUsecase,
        votes_repository=votes_repository,
        meps_repository=meps_repository,
        amendments_repository=amendments_repository
    )

    get_all_meps_usecase = providers.Factory(
        GetAllMepsUsecase,
        meps_repository=meps_repository,
    )

    get_mep_votes_usecase = providers.Factory(
        GetMEPVotesUsecase,
        meps_repository=meps_repository,
    )
