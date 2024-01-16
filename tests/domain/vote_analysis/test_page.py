import os
from typing import List

import pytest
from pypdf import PdfReader

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

def test_old_minutes_create_pages_with_no_header_from_pdf_return_correct_pages(old_minutes_pages_list):
    # given
    expected_page_id = 0
    expected_footer = "P9_PV(2019)11-14(RCV)_FR.docx 1 PE 643.960"
    path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "../../data/domain/vote_analysis/old_minutes_text_page_0.txt"
    )
    with open(path, mode='r') as f:
        expected_text = f.read()
    # when
    actual_page = Page(id=0, text=old_minutes_pages_list[expected_page_id])
    # then
    assert expected_page_id == actual_page.id
    assert expected_text == actual_page.text
    assert expected_footer == actual_page.footer
    assert actual_page.header is None

def test_new_minutes_create_pages_with_no_header_from_pdf_return_correct_pages(new_minutes_pages_list):
    # given
    expected_page_id = 0
    expected_footer = "P9_PV(2023)07-12(RCV)_FR.docx 1 PE 751.378"
    path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "../../data/domain/vote_analysis/new_minutes_text_page_0.txt"
    )
    with open(path, mode='r') as f:
        expected_text = f.read()
    # when
    actual_page = Page(id=0, text=new_minutes_pages_list[expected_page_id])
    # then
    assert expected_page_id == actual_page.id
    assert expected_text == actual_page.text
    assert expected_footer == actual_page.footer
    assert actual_page.header is None

def test_old_minutes_create_pages_with_header_from_pdf_return_correct_pages(old_minutes_pages_list):
    # given
    expected_page_id = 3
    expected_footer = "P9_PV(2019)11-14(RCV)_FR.docx 4 PE 643.960"
    expected_header = "1. A9-0019/2019 -  Ondřej Kovařík - Vote unique 14/11/2019 11:38:20.000"
    path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "../../data/domain/vote_analysis/old_minutes_text_page_3.txt"
    )
    with open(path, mode='r') as f:
        expected_text = f.read()
    # when
    actual_page = Page(id=3, text=old_minutes_pages_list[expected_page_id])
    # then
    assert expected_page_id == actual_page.id
    assert expected_text == actual_page.text
    assert expected_footer == actual_page.footer
    assert actual_page.header == expected_header


def test_new_minutes_create_pages_with_header_from_pdf_return_correct_pages(new_minutes_pages_list):
    # given
    expected_page_id = 6
    expected_footer = "P9_PV(2023)07-12(RCV)_FR.docx 7 PE 751.378"
    expected_header = "1. Règlement sur l’écoconception - A9-0218/2023 - Alessandra Moretti - Amendements de la commission compétente - vote par division et vote séparé - Am 34/2"
    path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "../../data/domain/vote_analysis/new_minutes_text_page_6.txt"
    )
    with open(path, mode='r') as f:
        expected_text = f.read()
    # when
    actual_page = Page(id=6, text=new_minutes_pages_list[expected_page_id])
    # then
    assert expected_page_id == actual_page.id
    assert expected_text == actual_page.text
    assert expected_footer == actual_page.footer
    assert actual_page.header == expected_header

def test_old_minutes_extract_amendment_name_from_header_return_correct_name(old_minutes_pages_list):
    # given
    expected_page_id = 3
    expected_name = "A9-0019/2019 -  Ondřej Kovařík - Vote unique"
    # when
    actual_page = Page(id=3, text=old_minutes_pages_list[expected_page_id])
    # then
    assert expected_name == actual_page.extract_amendment_name_from_header()

def test_new_minutes_extract_amendment_name_from_header_return_correct_name(new_minutes_pages_list):
    # given
    expected_page_id = 6
    expected_name = "Règlement sur l’écoconception - A9-0218/2023 - Alessandra Moretti - Amendements de la commission compétente - vote par division et vote séparé - Am 34/2"
    # when
    actual_page = Page(id=6, text=new_minutes_pages_list[expected_page_id])
    # then
    assert expected_name == actual_page.extract_amendment_name_from_header()

def test_page_with_small_id_smaller_than_page_whith_greater_id(old_minutes_pages_list):
    # given
    expected_small_id = 0
    expected_large_id = 1
    # when
    small_page = Page(id=expected_small_id, text=old_minutes_pages_list[0])
    large_page = Page(id=expected_large_id, text=old_minutes_pages_list[1])
    # then
    assert small_page < large_page


def test_header_extraction_works_for_multiple_headers(pages_list_new_header, pages_list_old_header):
    # given
    header_1 = "3. Règles communes visant à promouvoir la réparation des biens - Common rules promoting the repair of goods  - Gemeinsame \nVorschriften zur Förderung der Reparatur von Waren - A9-0316/2023 - René Repasi - Amendements de la commission compétente - vote \nséparé - Am 1"
    header_2 = "1. A9-0019/2019 -  Ondřej Kovařík - Vote unique 14/11/2019 11:38:20.000\n"
    expected_new_header = header_1
    expected_old_header = header_2

    # when
    test_new_page = Page(id=10, text=pages_list_new_header[10])
    test_old_page = Page(id=3, text=pages_list_old_header[3])
    actual_new_header = test_new_page.header
    actual_old_header = test_old_page.header

    # then
    assert actual_new_header == expected_new_header
    assert actual_old_header == expected_old_header
