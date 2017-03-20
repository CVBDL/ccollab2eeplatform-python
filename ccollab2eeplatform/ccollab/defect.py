"""Code ccollaborator defect records."""

import csv
import subprocess
import tempfile
import urllib.parse

from ccollab2eeplatform.log import logger


__all__ = ('csv_column_index', 'download_csv')


csv_column_index = {
    'defect_id': 0,
    'review_id': 1,
    'review_creation_date': 2,
    'creator_login': 3,
    'creator_full_name': 4,
    'severity': 5,
    'type_cvb': 6,
    'injection_stage': 7
}


def _create_download_command(creation_date_lo, creation_date_hi):
    """Create a full command used to download defect CSV from ccollab."""
    creation_date_filter = {
        'reviewCreationDateFilter': 'lo={0}|||hi={1}'.format(creation_date_lo,
                                                             creation_date_hi)
    }
    command = ''.join([
        'ccollab admin wget \"/go?',
        'type_cvbVis=y',
        '&defectIdVis=y',
        '&severityVis=y',
        '&defectReviewIdVis=y',
        '&defectCreatorUserNameVis=y',
        '&reviewCreatedVis=y',
        '&defectCreatorUserLoginVis=y',
        '&injectionStageVis=y',
        '&page=ReportDefectList',
        '&component=ErrorsAndMessages',
        '&data-format=csv',
        '&groupDepth=0',
        '&formSubmittedreportConfig=1',
        '&' + urllib.parse.urlencode(creation_date_filter),
        '\"'
    ])
    return command


def download_csv(creation_date_lo, creation_date_hi):
    """Download defect CSV into a temp file."""
    command = _create_download_command(creation_date_lo, creation_date_hi)
    defect_records = []

    # The downloaded CSV file is 'utf-8-sig' encoded.
    # utf-8:     'ABC'
    # utf-8-sig: '\xef\xbb\xbfABC'
    #with tempfile.TemporaryFile(mode='w+', encoding='utf-8-sig') as temp_csv:
    #    subprocess.run(command, shell=True, stdout=temp_csv)
    #    defect_reader = csv.reader(temp_csv, delimiter=',')
    #    for row in defect_reader:
    #        print(row)

    import os
    filepath = os.path.dirname(__file__) + './defects-report.csv'
    with open(filepath) as temp_csv:
        defect_reader = csv.reader(temp_csv, delimiter=',')
        # Skip CSV header row
        next(defect_reader)
        for row in defect_reader:
            defect_records.append(row)

    return defect_records
