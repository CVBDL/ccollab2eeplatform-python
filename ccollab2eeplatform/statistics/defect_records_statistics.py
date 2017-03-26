"""Defect records statistics module."""

from itertools import groupby

from ccollab2eeplatform.settings.users_settings import UsersSettings
from ccollab2eeplatform.filters.creator_filter import CreatorFilter


class DefectRecordsStatistics:
    """Defect records statistics class.

    Args:
        records: A list of defect record.
    Attributes:
        records: A list of defect record.
    """

    def __init__(self, records):
        self.records = records

    def calc_defect_count_by_product(self):
        """Defect count by product.

        Data table:
        Product  Count
        Team1    20
        Team2    16

        Returns:
            A tuple of column definition and data.
        """
        schema = [('Product', 'string'), ('Count', 'number')]
        data = []

        creator_filter = CreatorFilter(self.records,
                                       UsersSettings.list_login_names())
        for key, group in groupby(
                creator_filter.filter(),
                lambda record: record.creator_product_name):

            data.append([key, sum(1 for _ in group)])

        return schema, data