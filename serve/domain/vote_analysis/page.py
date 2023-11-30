import re

from pydantic import BaseModel, model_validator


def get_mep_full_name_and_group(name: str, group_name: str):
    """ TO IMPLEMENT"""
    return name, group_name

class Page(BaseModel):
    id: int
    text: str
    header: str = None
    footer: str = None

    def _build_footer_regex(self) -> str:
        regex_footer = r"^.*\d{3}\.\d{3}"
        found_footer = re.findall(regex_footer, self.text)
        if len(found_footer) != 1:
            raise Exception(f"Error extracting footer, should have exactly one match but got {len(found_footer)}")
        splited_footer = found_footer[0].split()
        footer_regex = re.escape(splited_footer[0]) + r"\s\d+.*?" + re.escape(splited_footer[-1])
        return footer_regex

    @model_validator(mode="after")
    def extract_footer(self) -> "Page":
        if self.footer is None:
            footer_regex = self._build_footer_regex()
            footer_found = re.findall(footer_regex, self.text)
            if len(footer_found) == 1:
                self.footer = footer_found[0]
                self.text = re.split(footer_regex, self.text)[1]
            elif len(footer_found) > 1:
                raise Exception('Error extracting footer, found multiple match.')
        return self

    @model_validator(mode="after")
    def extract_header(self) -> "Page":
        if self.header is None:
            header_regex = r"^\d+\.\s.+\s\d{1,2}/\d{1,2}/\d{4}\s\d{2}:\d{2}:\d{2}.\d{3}\n"
            header_found = re.findall(header_regex, self.text)
            if len(header_found) == 1:
                self.header = header_found[0]
                self.text = re.split(header_regex, self.text)[1]
            elif len(header_found) > 1:
                raise Exception('Error extracting header, found multiple match.')
        return self

    def __lt__(self, other: "Page"):
        return self.id < other.id

    def extract_amendment_name_from_header(self):
        if self.header is None:
            return None
        extract_regex = r"^\d+\.\s(.+)\s\d{1,2}/\d{1,2}/\d{4}\s\d{2}:\d{2}:\d{2}.\d{3}\n"
        amendment_name = re.findall(extract_regex, self.header)[0]
        return amendment_name
