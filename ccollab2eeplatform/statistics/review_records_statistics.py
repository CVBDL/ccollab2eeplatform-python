"""Code review records statistics module."""

from itertools import groupby

from ccollab2eeplatform import utils
from ccollab2eeplatform.filters.creator_filter import CreatorFilter
from ccollab2eeplatform.settings.users_settings import UsersSettings
from ccollab2eeplatform.statistics.records_statistics import RecordsStatistics


class ReviewRecordsStatistics(RecordsStatistics):
    """Review records statistics class.

    Args:
        records: A list of review record.
    """

    def __init__(self, records):
        super().__init__(records)
        self._records = records
