import os
from typing import List

import pytest
from pypdf import PdfReader

from serve.domain.vote_analysis.amendment import Minutes, MinutesAggregate
from serve.domain.vote_analysis.page import Page


@pytest.fixture
def pages_list() -> List[str]:
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../data/domain/vote_analysis/test_minutes.pdf")
    with open(path, "rb") as f:
        pdf = PdfReader(f)
        pages_list = []
        for page in pdf.pages:
            page_text = page.extract_text()
            pages_list.append(page_text)
    return pages_list

def test_creation_from_list_str_return_correct_minutes(pages_list):
    # given
    expected_page_number = 73
    expected_amendment_number = 35
    expected_first_amendment_id = "A9-0019/2019 -  Ondřej Kovařík - Vote unique"
    expected_first_amendment_minutes_id = "test_minutes"
    expected_first_amendment_page_numbers = 2
    # when
    actual_minutes = Minutes(id="test_minutes", pages_list=[Page(id=i, text=text) for i, text in enumerate(pages_list)])
    actual_first_amendment = actual_minutes.amendments_list[0]
    # then
    assert expected_page_number == len(actual_minutes.pages_list)
    assert expected_amendment_number == len(actual_minutes.amendments_list)
    assert expected_first_amendment_id == actual_first_amendment.id
    assert expected_first_amendment_minutes_id == actual_first_amendment.minutes_id
    assert expected_first_amendment_page_numbers == len(actual_first_amendment.pages)

def test_extract_votes_from_amendments_return_correct_votes(pages_list):
    # given
    expected_amendment_id = "A9-0019/2019 -  Ondřej Kovařík - Vote unique"
    expected_amendment_vote_numbers = 653
    expected_amendment_for_votes = 565
    expected_amendment_against_votes = 23
    expected_amendment_null_votes = 65
    # when
    actual_minutes = Minutes(id="test_minutes", pages_list=[Page(id=i, text=text) for i, text in enumerate(pages_list)])
    actual_votes = MinutesAggregate.extract_votes_from_amendments(actual_minutes, amendment_ids=expected_amendment_id)
    actual_for_votes = len([vote for vote in actual_votes if vote.value == "+"])
    actual_against_votes = len([vote for vote in actual_votes if vote.value == "-"])
    actual_null_votes = len([vote for vote in actual_votes if vote.value == "0"])
    # then
    assert expected_amendment_vote_numbers == len(actual_votes)
    assert expected_amendment_for_votes == actual_for_votes
    assert expected_amendment_against_votes == actual_against_votes
    assert expected_amendment_null_votes == actual_null_votes