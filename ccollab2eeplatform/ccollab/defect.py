"""Code ccollaborator defect records."""

import csv
import subprocess
import tempfile
import urllib.parse

from ccollab2eeplatform.log import logger
from ccollab2eeplatform.ccollab.defect_record import DefectRecord


__all__ = ('fetch_defect_records')


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


def fetch_defect_records(creation_date_lo, creation_date_hi):
    """Download defect CSV into a temp file."""
    command = _create_download_command(creation_date_lo, creation_date_hi)
    defect_records = []

    # The downloaded CSV file is 'utf-8-sig' encoded.
    # utf-8:     'ABC'
    # utf-8-sig: '\xef\xbb\xbfABC'
    #with tempfile.TemporaryFile(mode='w+', encoding='utf-8-sig') as temp_csv:
    #    logger.info('Downloading defect CSV file ...')
    #    subprocess.run(command, shell=True, stdout=temp_csv)
    #    logger.info('Downloading defect CSV file ... Done')
    #    temp_csv.seek(0)
    #    defect_reader = csv.reader(temp_csv, delimiter=',')
    #    # skip header record
    #    try:
    #        next(defect_reader)
    #    except StopIteration:
    #        pass
    #    else:
    #        for record in defect_reader:
    #            defect_records.append(record)

    #return defect_records

    import os
    filepath = os.path.dirname(__file__) + './defects-report.csv'
    with open(filepath) as temp_csv:
        defect_reader = csv.reader(temp_csv, delimiter=',')
        # skip header row
        next(defect_reader)
        for record in defect_reader:
            defect_records.append(DefectRecord(record))

    return defect_records
