from unittest import mock

import pytest

from serve.domain.european_parliament.mep import GroupsEnum, MEP
from serve.domain.vote_analysis.mep import MEPReadFromMinutes
from serve.infra.repositories.amendments_sql_repository import AmendmentsSqlRepository
from serve.infra.repositories.meps_in_memory_repository import MepsInMemoryRepository
from serve.infra.repositories.votes_sql_repository import VotesSqlRepository
from serve.usecase.vote_analysis.extract_votes_from_minutes import ExtractVotesFromMinutesUsecase


@pytest.fixture
def extract_vote_usecase():
    meps_in_memory_repository = MepsInMemoryRepository()
    mock_votes_repository: VotesSqlRepository = mock.Mock(spec=VotesSqlRepository)
    mock_amendments_repository: AmendmentsSqlRepository = mock.Mock(spec=AmendmentsSqlRepository)
    extract_votes_usecase = ExtractVotesFromMinutesUsecase(
        votes_repository=mock_votes_repository,
        meps_repository=meps_in_memory_repository,
        amendments_repository=mock_amendments_repository
    )
    return extract_votes_usecase


def test_build_mep_from_name_returns_correct_mep_from_last_name_and_group(extract_vote_usecase):
    # Given
    expected_mep = MEP(
        id="1",
        full_name="John Doe",
        current_group_short_name=GroupsEnum.NI,
        country="France",
        is_active=True
    )
    mep = MEPReadFromMinutes(
        name="Doe",
        current_group_short_name=GroupsEnum.NI
    )

    # When
    corrected_name = extract_vote_usecase.build_mep_from_name(mep)
    # Then
    assert corrected_name.current_group_short_name == expected_mep.current_group_short_name


def test_build_mep_from_name_returns_correct_mep_from_last_name_and_group_when_group_changed(extract_vote_usecase):
    # Given
    expected_mep = MEP(
        id="1",
        full_name="John Doe",
        current_group_short_name=GroupsEnum.NI,
        country="France",
        is_active=True
    )

    mep = MEPReadFromMinutes(
        name="Doe",
        current_group_short_name=GroupsEnum.ID
    )
    # When
    corrected_name = extract_vote_usecase.build_mep_from_name(mep)
    # Then
    assert corrected_name.current_group_short_name == expected_mep.current_group_short_name
