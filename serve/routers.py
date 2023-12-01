from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import UploadFile, Depends, APIRouter

from container import Container
from serve.usecase.european_parliament.create_all_meps import CreateAllMepsUsecase
from serve.usecase.vote_analysis.extract_votes_from_minutes import ExtractVotesFromMinutesUsecase

router = APIRouter()


@router.post("/extract")
@inject
def extract_votes_from_pdf(minutes_pdf: UploadFile, amendments_list: List[str],
                           minutes_type: str,
                           url: str,
                           extract_votes_usecase: ExtractVotesFromMinutesUsecase = Depends(
                               Provide[Container.extract_votes_usecase]
                           )):
    return extract_votes_usecase.read_minutes_and_extract_votes(
        minutes_id=url,
        minutes_type=minutes_type,
        minutes_pdf=minutes_pdf.file,
        amendment_ids=amendments_list
    )


@router.post("/create_batch")
@inject
def create_batch_meps(
        create_batch_meps_usecase: CreateAllMepsUsecase = Depends(Provide[Container.create_all_meps_usecase])
):
    return create_batch_meps_usecase.load_all_meps()
