from typing import Generic, List, TypeVar

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query, UploadFile
from fastapi_pagination import Page, paginate
from fastapi_pagination.default import Page as BasePage
from fastapi_pagination.default import Params as BaseParams
from slowapi import Limiter
from slowapi.util import get_remote_address
from starlette.requests import Request

from container import Container
from serve.domain.european_parliament.mep import MEP
from serve.domain.vote_analysis.vote import NormalizedVote
from serve.usecase.european_parliament.create_all_meps import \
    CreateAllMepsUsecase
from serve.usecase.european_parliament.get_all_meps import GetAllMepsUsecase
from serve.usecase.vote_analysis.extract_votes_from_minutes import \
    ExtractVotesFromMinutesUsecase
from serve.usecase.vote_analysis.get_mep_votes import GetMEPVotesUsecase
from serve.usecase.vote_analysis.initialize_votes_extract import \
    InitializeVotesExtractUsecase

router = APIRouter()
limiter = Limiter(key_func=get_remote_address, default_limits=["2/5seconds"])

# T, Params and Page are needed to override default pagination of get_emissions_from_run
T = TypeVar("T")

class Params(BaseParams):
    # Default results to 100 to avoid crash in /docs
    size: int = Query(100, ge=1, le=10_000, description="Page size")


class Page(BasePage[T], Generic[T]):  # noqa: F811
    __params_type__ = Params


@router.post("/extract")
@inject
def extract_votes_from_pdf(minutes_pdf: UploadFile,
                           amendments_list: List[str],
                           minutes_type: str,
                           binding_value: int,
                           url: str,
                           extract_votes_usecase: ExtractVotesFromMinutesUsecase = Depends(
                               Provide[Container.extract_votes_usecase]
                           )):
    return extract_votes_usecase.read_minutes_and_extract_votes(
        minutes_id=url,
        minutes_type=minutes_type,
        binding_value=binding_value,
        minutes_pdf=minutes_pdf.file,
        amendment_ids=amendments_list[0].split(";")
    )


@router.post("/initialize")
@inject
def initialize_votes_extract(init_file: UploadFile,
                             initialize_votes_extract: InitializeVotesExtractUsecase = Depends(
                                 Provide[Container.initialize_votes_extract]
                             )):
    return initialize_votes_extract.read_file_and_extract_votes(init_file=init_file)

@router.post("/create_batch")
@inject
def create_batch_meps(
        create_batch_meps_usecase: CreateAllMepsUsecase = Depends(Provide[Container.create_all_meps_usecase])
):
    return create_batch_meps_usecase.load_all_meps()

@router.get('/MEPs', response_model=Page[MEP])
@limiter.limit("1/seconds")
@inject
async def get_meps(
    request: Request,
    get_all_meps_usecase: GetAllMepsUsecase = Depends(Provide[Container.get_all_meps_usecase])
):
    return paginate(get_all_meps_usecase.get_all_meps())

@router.get('/votes', response_model=Page[NormalizedVote])
@limiter.limit("1/seconds")
@inject
def get_votes(
        request: Request,
        mep_id: int,
        get_mep_votes_usecase: GetMEPVotesUsecase = Depends(Provide[Container.get_mep_votes_usecase]),
        params: Params = Depends(),
):
    return paginate(get_mep_votes_usecase.get_mep_votes(mep_id), params)
