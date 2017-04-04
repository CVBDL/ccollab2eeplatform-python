"""Records statistics module."""

from itertools import groupby


class RecordsStatistics:
    """Review records statistics class.

    Args:
        records: A list of record.
    """

    def __init__(self, records):
        self._records = records

    def calc_count_by_month(self):
        """Record count by month.

        Data table:
        Month    Count
        2016-01  20
        2016-03  10
        2016-05  25

        Returns:
            A tuple of column definition and data.
        """
        schema = [('Month', 'string'), ('Count', 'number')]
        data = []
        def keyfunc(record):
            return record.review_creation_month
        for key, group in groupby(sorted(self._records, key=keyfunc),
                                  keyfunc):
            data.append([key, sum(1 for _ in group)])
        return schema, data

    def calc_count_by_product(self):
        """Record count by product.

        Data table:
        Product  Count
        Team1    20
        Team2    16

        Returns:
            A tuple of column definition and data.
        """
        schema = [('Product', 'string'), ('Count', 'number')]
        data = []
        def keyfunc(record):
            return record.creator_product_name
        for key, group in groupby(sorted(self._records, key=keyfunc),
                                  keyfunc):
            data.append([key, sum(1 for _ in group)])
        return schema, data
