import io
from typing import Any, Dict, List
from urllib.request import Request, urlopen

import pandas as pd

from serve.domain.european_parliament.mep import MEPs
from serve.domain.vote_analysis.minutes import (Amendments, Minutes,
                                                MinutesAggregate)
from serve.domain.vote_analysis.vote import NormalizedVote, Vote, Votes
from serve.logger import logger
from serve.usecase.vote_analysis.extract_votes_from_minutes import \
    ExtractVotesFromMinutesUsecase


class InitializeVotesExtractUsecase(ExtractVotesFromMinutesUsecase):
    def __init__(self, votes_repository: Votes, meps_repository: MEPs, amendments_repository: Amendments):
        super().__init__(votes_repository, meps_repository, amendments_repository)

    def read_file_and_extract_votes(self, init_file: Any):
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
                normalized_votes = self.check_duplicate_meps_amendment(normalized_votes, votes)
                self.amendments_repository.save_amendments(minutes, amendment_ids)
                self.votes_repository.save_votes(normalized_votes)
            except Exception as e:
                logger.warning(f"Can't extract votes for minutes {minutes.id} and amendment_ids {amendment_ids} ({e})")

    def read_pdf_from_url(self, url):
        return io.BytesIO(urlopen(Request(url)).read())

    def read_file_and_extract_minutes_and_amendment_name(self, df_init: pd.DataFrame) -> Dict[Minutes, List[str]]:
        minutes_amendment_ids = {}
        for id, row in df_init.iterrows():
            try:
                if pd.notna(row.ID):
                    # read pdf and store each page extracted text in a list
                    pdf_url = row.ID.split('.pdf')[0] + '.pdf'
                    minutes_pdf = self.read_pdf_from_url(pdf_url)
                    minutes = self.convert_minutes_from_pdf(pdf_url,
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
                logger.warning(f"Cannot read amendment in row {id}: p.{row.Page} - {row.ID} : {e}")
        logger.info(f"{len([item for sublist in minutes_amendment_ids.values() for item in sublist])} amendments loaded")
        return minutes_amendment_ids

    def check_duplicate_meps_amendment(self, normalized_votes: List[NormalizedVote], votes=List[Vote]):
        # Create a set to keep track of unique elements
        seen_amendment_mep = {}
        duplicates = {}
        already_detected_duplicates = {}
        to_remove = []
        for i, normalized_vote in enumerate(normalized_votes):
            amendment_id = normalized_vote.amendment_id
            med_id = normalized_vote.mep.id
            key = (amendment_id, med_id)
            if key in seen_amendment_mep:
                mep = seen_amendment_mep[key][1].mep
                if key not in already_detected_duplicates:
                    duplicates.setdefault(amendment_id, {})
                    duplicates[amendment_id][mep] = [votes[seen_amendment_mep[key][0]]]
                    already_detected_duplicates[key] = True
                    to_remove.append(seen_amendment_mep[key][1])
                duplicates[amendment_id][mep].append(votes[i])
                to_remove.append(normalized_vote)
            else:
                seen_amendment_mep[key] = (i, normalized_vote)
        if len(to_remove) > 0:
            logger.warning(f"Removing {len(to_remove)} votes with duplicated meps for the same amendment.")
            logger.warning(f"Duplicated amendment and mep : {duplicates}")
            return [vote for vote in normalized_votes if vote not in to_remove]
        return normalized_votes
