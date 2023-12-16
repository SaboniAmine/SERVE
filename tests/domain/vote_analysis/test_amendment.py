import os
from typing import List

import pytest
from pypdf import PdfReader

from serve.domain.vote_analysis.minutes import Amendment
from serve.domain.vote_analysis.page import Page


@pytest.fixture
def old_minutes_pages_list() -> List[str]:
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../data/domain/vote_analysis/old_minutes.pdf")
    with open(path, "rb") as f:
        pdf = PdfReader(f)
        pages_list = []
        for page in pdf.pages:
            page_text = page.extract_text()
            pages_list.append(page_text)
    return pages_list

@pytest.fixture
def new_minutes_pages_list() -> List[str]:
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../data/domain/vote_analysis/new_minutes.pdf")
    with open(path, "rb") as f:
        pdf = PdfReader(f)
        pages_list = []
        for page in pdf.pages:
            page_text = page.extract_text()
            pages_list.append(page_text)
    return pages_list


def test_create_amendment_return_correct_amendment(old_minutes_pages_list):
    # given
    expected_id = "amendment_id"
    expected_minutes_id = "minutes_id"
    expected_pages = [Page(id=i, text=text) for i, text in enumerate(old_minutes_pages_list[3:5])]
    expected_page_numbers = 2
    # when
    actual_amendment = Amendment(id="amendment_id", minutes_id="minutes_id", pages=expected_pages)
    # then
    assert expected_id == actual_amendment.id
    assert expected_minutes_id == actual_amendment.minutes_id
    assert expected_page_numbers == len(actual_amendment.pages)


def test_old_minutes_get_str_amendment_votes_return_correct_str(old_minutes_pages_list):
    # given
    path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "../../data/domain/vote_analysis/old_minutes_extracted_votes.txt"
    )
    with open(path, mode='r') as f:
        expected_vote_str = f.read()
    # when
    actual_amendment = Amendment(
        id="amendment_id",
        minutes_id="minutes_id",
        pages=[Page(id=i, text=text) for i, text in enumerate(old_minutes_pages_list[3:5])]
    )
    # then
    assert expected_vote_str == actual_amendment.get_str_amendment_votes()

def test_new_minutes_get_str_amendment_votes_return_correct_str(new_minutes_pages_list):
    # given
    path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "../../data/domain/vote_analysis/new_minutes_extracted_votes.txt"
    )
    with open(path, mode='r') as f:
        expected_vote_str = f.read()
    # when
    actual_amendment = Amendment(
        id="amendment_id",
        minutes_id="minutes_id",
        pages=[Page(id=i, text=text) for i, text in enumerate(new_minutes_pages_list[6:8])]
    )
    # then
    assert expected_vote_str == actual_amendment.get_str_amendment_votes()