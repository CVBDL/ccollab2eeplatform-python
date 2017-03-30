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
        self._valid_records = None

    def _get_valid_records(self):
        """Return records which we should use to calculate statistics.

        Only the record which creator login name is in users settings
        file is considered to be valid.
        """
        if self._valid_records is None:
            valid_creator_filter = CreatorFilter(
                self.records,
                UsersSettings.list_login_names()
            )
            self._valid_records = valid_creator_filter.filter()

        return self._valid_records

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
        valid_records = self._get_valid_records()
        keyfunc = lambda record: record.review_creation_month
        for key, group in groupby(
                sorted(valid_records, key=keyfunc), keyfunc):
            data.append([key, sum(1 for _ in group)])

        return schema, data

    def calc_review_count_by_product(self):
        """Review count by product.

        Data table:
        Product  Count
        Team1    20
        Team2    16

        Returns:
            A tuple of column definition and data.
        """
        schema = [('Product', 'string'), ('Count', 'number')]
        data = []
        valid_records = self._get_valid_records()
        keyfunc = lambda record: record.creator_product_name
        for key, group in groupby(
                sorted(valid_records, key=keyfunc), keyfunc):
            data.append([key, sum(1 for _ in group)])

        return schema, data
