import pytest
from pydantic import ValidationError

from serve.domain.vote_analysis.deputy import Deputy
from serve.domain.vote_analysis.vote import Vote


@pytest.fixture
def deputy() -> Deputy:
    return Deputy(id="John_Doe_ECR", name="John Doe", actual_group="ECR", group_at_time="Renew")

def test_create_vote_return_correct_vote(deputy):
    # given
    expected_amendment_id = "amendment_id"
    expected_value = "+"
    expected_deputy = deputy
    # when
    actual_vote = Vote(amendment_id="amendment_id", value="+", deputy=deputy)
    # then
    assert expected_amendment_id == actual_vote.amendment_id
    assert expected_value == actual_vote.value
    assert expected_deputy == actual_vote.deputy

def test_create_vote_with_unexpected_value_fails(deputy):
    # given
    fail_value = "*"
    # then
    with pytest.raises(ValidationError):
        # when
        Vote(amendment_id="1", value=fail_value, deputy=deputy)
