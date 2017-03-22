"""Code ccollaborator review records."""

import csv
import subprocess
import tempfile
import urllib.parse

from ccollab2eeplatform.log import logger
from ccollab2eeplatform.ccollab.review_record import ReviewRecord


__all__ = ('fetch_review_records')


def _create_download_command(creation_date_lo, creation_date_hi):
    """Create a full command used to download review CSV from ccollab."""
    creation_date_filter = {
        'reviewCreationDateFilter': 'lo={0}|||hi={1}'.format(creation_date_lo,
                                                             creation_date_hi)
    }
    command = ''.join([
        'ccollab admin wget \"/go?',
        'reviewCreatorUserLoginVis=y',
        '&numDefectsVis=y',
        '&reviewCreatorUserNameVis=y',
        '&reviewIdVis=y',
        '&reviewPersonDurationVis=y',
        '&reviewCreationDateVis=y',
        '&numCommentsVis=y',
        '&locVis=y',
        '&locChangedVis=y',
        '&data-format=csv',
        '&page=ReportReviewList',
        '&formSubmittedreportConfig=1',
        '&' + urllib.parse.urlencode(creation_date_filter),
        '\"'
    ])
    return command


def fetch_review_records(creation_date_lo, creation_date_hi):
    """Download review CSV into a temp file."""
    command = _create_download_command(creation_date_lo, creation_date_hi)
    review_records = []

    # The downloaded CSV file is 'utf-8-sig' encoded.
    # utf-8:     'ABC'
    # utf-8-sig: '\xef\xbb\xbfABC'
    #with tempfile.TemporaryFile(mode='w+', encoding='utf-8-sig') as temp_csv:
    #    logger.info('Downloading review CSV file ...')
    #    subprocess.run(command, shell=True, stdout=temp_csv)
    #    logger.info('Downloading review CSV file ... Done')
    #    temp_csv.seek(0)
    #    review_reader = csv.reader(temp_csv, delimiter=',')
    #    # skip header record
    #    try:
    #        next(review_reader)
    #    except StopIteration:
    #        pass
    #    else:
    #        for record in review_reader:
    #            review_records.append(record)

    #return review_records

    import os
    filepath = os.path.dirname(__file__) + './reviews-report.csv'
    with open(filepath) as temp_csv:
        review_reader = csv.reader(temp_csv, delimiter=',')
        # skip header row
        next(review_reader)
        for record in review_reader:
            review_records.append(ReviewRecord(record))

    return review_records
