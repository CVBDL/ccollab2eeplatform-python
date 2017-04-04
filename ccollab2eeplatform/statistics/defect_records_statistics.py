"""Defect records statistics module."""

from itertools import groupby

from ccollab2eeplatform.settings.users_settings import UsersSettings
from ccollab2eeplatform.filters.creator_filter import CreatorFilter
from ccollab2eeplatform.statistics.records_statistics import RecordsStatistics


class DefectRecordsStatistics(RecordsStatistics):
    """Defect records statistics class.

    Args:
        records: A list of defect record.
    Attributes:
        records: A list of defect record.
    """

    def __init__(self, records):
        super().__init__(records)
        self._records = records
