import io
from typing import Any, Dict, List

import pandas as pd
from urllib.request import Request, urlopen

from serve.domain.european_parliament.mep import MEPs
from serve.domain.vote_analysis.minutes import Minutes, MinutesAggregate, Amendments
from serve.domain.vote_analysis.vote import Votes
from serve.logger import logger
from serve.usecase.vote_analysis.extract_votes_from_minutes import ExtractVotesFromMinutesUsecase


class InitializeVotesExtractUsecase(ExtractVotesFromMinutesUsecase):
    def __init__(self, votes_repository: Votes, meps_repository: MEPs, amendments_repository: Amendments):
        super().__init__(votes_repository, meps_repository, amendments_repository)

    def read_file_and_extract_votes(self, init_file: Any):
        exceptions = []
        contents = init_file.file.read()
        data = io.BytesIO(contents)
        df_init = pd.read_excel(data)
        logger.info(f"{len(df_init)} amendments to ingest")
        minutes_amendment_ids = self.read_file_and_extract_minutes_and_amendment_name(df_init)
        logger.info('Done extracting minutes and amendment names from file')
        for minutes, amendment_ids in minutes_amendment_ids.items():
            try:
                votes = MinutesAggregate.extract_votes_from_amendments(minutes, amendment_ids)
                normalized_votes = self.normalized_votes_read_from_minutes(votes)
                self.amendments_repository.save_amendments(minutes, amendment_ids)
                self.votes_repository.save_votes(normalized_votes)
            except Exception as e:
                exceptions.append(
                    f"Can't extract votes for minutes {minutes.id} and amendment_ids {amendment_ids} ({e})")
                # logger.warning(f"Can't extract votes for minutes {minutes.id} and amendment_ids {amendment_ids} ({e})")
        print(exceptions)

    def read_pdf_from_url(self, url):
        return io.BytesIO(urlopen(Request(url)).read())

    def read_file_and_extract_minutes_and_amendment_name(self, df_init: pd.DataFrame) -> Dict[Minutes, List[str]]:
        minutes_amendment_ids = {}
        for id, row in df_init.iterrows():
            try:
                if pd.notna(row.ID):
                    # read pdf and store each page extracted text in a list
                    minutes_pdf = self.read_pdf_from_url(row.ID)
                    minutes_id = row.ID.split('.pdf')[0] + '.pdf'
                    minutes = self.convert_minutes_from_pdf(minutes_id,
                                                            row.Subject_Sarah,
                                                            row["Binding value"],
                                                            minutes_pdf)
                    amendment_id_to_extract = [
                        amendment.id
                        for amendment in minutes.amendments_list
                        if min(amendment.pages).id + 1 == row.Page
                    ]

                    if len(amendment_id_to_extract) == 0:
                        logger.warning(
                            f'No amendment found for row {id}: p.{row.Page} - {row.ID}, check the specified page number.')
                    else:
                        minutes_amendment_ids.setdefault(minutes, []).append(amendment_id_to_extract[0])
                else:
                    logger.warning(f'Missing URL for row {id} ({row.Text}).')
            except Exception as e:
                print(f"Cannot read amendment in row {id}: p.{row.Page} - {row.ID} : {e}")
        logger.info(
            f"{len([item for sublist in minutes_amendment_ids.values() for item in sublist])} amendments loaded")
        return minutes_amendment_ids
