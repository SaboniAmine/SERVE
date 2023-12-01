from typing import List

import requests
from xmltodict import parse

from serve.domain.european_parliament.mep import EuropeanParliamentMEPSource, EuropeanParliamentMEP


class XmlEuropeanParliamentMEPSource(EuropeanParliamentMEPSource):
    def __init__(self, mep_list_source):
        self.mep_list_source = mep_list_source

    def get_updated_list(self) -> List[EuropeanParliamentMEP]:
        response = requests.get(self.mep_list_source)
        meps_raw_list = parse(response.content)

        return [
            EuropeanParliamentMEP(
                id=mep["id"],
                full_name=mep["fullName"],
                country=mep["country"],
                group_full_name=mep["politicalGroup"],
                national_political_group=mep["nationalPoliticalGroup"],
            )
            for mep in meps_raw_list['meps']["mep"]
        ]
