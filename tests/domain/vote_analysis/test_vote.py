import pytest
from pydantic import ValidationError

from serve.domain.vote_analysis.mep import MEP
from serve.domain.vote_analysis.vote import Vote


@pytest.fixture
def mep() -> MEP:
    return MEP(name="foo", current_group_short_name="ECR")

def test_create_vote_return_correct_vote(mep):
    # given
    expected_amendment_id = "amendment_id"
    expected_value = "+"
    expected_mep = mep
    # when
    actual_vote = Vote(amendment_id="amendment_id", mep=mep, value="+")
    # then
    assert expected_amendment_id == actual_vote.amendment_id
    assert expected_value == actual_vote.value
    assert expected_mep == actual_vote.mep

def test_create_vote_with_unexpected_value_fails(mep):
    # given
    fail_value = "*"
    # then
    with pytest.raises(ValidationError):
        # when
        Vote(amendment_id="1", mep=mep, value=fail_value)
