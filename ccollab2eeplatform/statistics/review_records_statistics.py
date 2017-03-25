"""Code review records statistics module."""

from itertools import groupby

from ccollab2eeplatform.settings.users_settings import UsersSettings
from ccollab2eeplatform.filters.creator_filter import CreatorFilter


class ReviewRecordsStatistics:
    """Review records statistics class.

    Args:
        records: A list of review record.
    Attributes:
        records: A list of review record.
    """

    def __init__(self, records):
        self.records = records

    def calc_review_count_by_month(self):
        """Review count by month.

        Data table:
        Month    Count
        2016-01  20
        2016-02  30
        2016-03  25

        Returns:
            A tuple of column definition and data.
        """
        schema = [('Month', 'string'), ('Count', 'number')]
        data = []

        creator_filter = CreatorFilter(self.records,
                                       UsersSettings.list_login_names())
        for key, group in groupby(
                creator_filter.filter(),
                lambda record: record.review_creation_month):

            data.append([key, sum(1 for _ in group)])

        return schema, data
