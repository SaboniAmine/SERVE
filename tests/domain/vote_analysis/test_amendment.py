import os
from typing import List

import pytest
from pypdf import PdfReader

from serve.domain.vote_analysis.minutes import Amendment, Page


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


def test_create_amendment_return_correct_amendment(pages_list):
    # given
    expected_id = "amendment_id"
    expected_pdf_id = "pdf_id"
    expected_pages = [Page(id=i, text=text) for i, text in enumerate(pages_list[3:5])]
    expected_page_numbers = 2
    expected_vote_numbers = 653
    expected_for_votes = 565
    expected_against_votes = 23
    expected_null_votes = 65
    # when
    actual_amendment = Amendment(id="amendment_id", pdf_id="pdf_id", pages=expected_pages)
    actual_for_votes = len([vote for vote in actual_amendment.votes if vote.value == "+"])
    actual_against_votes = len([vote for vote in actual_amendment.votes if vote.value == "-"])
    actual_null_votes = len([vote for vote in actual_amendment.votes if vote.value == "0"])
    # then
    assert expected_id == actual_amendment.id
    assert expected_pdf_id == actual_amendment.pdf_id
    assert expected_page_numbers == len(actual_amendment.pages)
    assert expected_vote_numbers == len(actual_amendment.votes)
    assert expected_for_votes == actual_for_votes
    assert expected_against_votes == actual_against_votes
    assert expected_null_votes == actual_null_votes
