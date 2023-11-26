import os
from typing import List

import pytest
from pypdf import PdfReader

from serve.domain.vote_analysis.minutes import Page


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

def test_create_pages_with_no_header_from_pdf_return_correct_pages(pages_list):
    # given
    expected_page_id = 0
    expected_footer = "P9_PV(2019)11-14(RCV)_FR.docx 1 PE 643.960"
    path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "../../data/domain/vote_analysis/extracted_text_page_0.txt"
    )
    with open(path, mode='r') as f:
        expected_text = f.read()
    # when
    actual_page = Page(id=0, text=pages_list[expected_page_id])
    # then
    assert expected_page_id == actual_page.id
    assert expected_text == actual_page.text
    assert expected_footer == actual_page.footer
    assert actual_page.header is None

def test_create_pages_with_header_from_pdf_return_correct_pages(pages_list):
    # given
    expected_page_id = 3
    expected_footer = "P9_PV(2019)11-14(RCV)_FR.docx 4 PE 643.960"
    expected_header = "1. A9-0019/2019 -  Ondřej Kovařík - Vote unique 14/11/2019 11:38:20.000\n"
    path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "../../data/domain/vote_analysis/extracted_text_page_3.txt"
    )
    with open(path, mode='r') as f:
        expected_text = f.read()
    # when
    actual_page = Page(id=3, text=pages_list[expected_page_id])
    # then
    assert expected_page_id == actual_page.id
    assert expected_text == actual_page.text
    assert expected_footer == actual_page.footer
    assert actual_page.header == expected_header

def test_extract_amendment_name_from_header_return_correct_name(pages_list):
    # given
    expected_page_id = 3
    expected_name = "A9-0019/2019 -  Ondřej Kovařík - Vote unique"
    # when
    actual_page = Page(id=3, text=pages_list[expected_page_id])
    # then
    assert expected_name == actual_page.extract_amendment_name_from_header()

def test_page_with_small_id_smaller_than_page_whith_greater_id(pages_list):
    # given
    expected_small_id = 0
    expected_large_id = 1
    # when
    small_page = Page(id=expected_small_id, text=pages_list[0])
    large_page = Page(id=expected_large_id, text=pages_list[1])
    # then
    assert small_page < large_page
