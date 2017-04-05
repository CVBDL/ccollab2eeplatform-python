"""Records statistics module."""

from itertools import groupby

from ccollab2eeplatform import utils


class RecordsStatistics:
    """Review records statistics class.

    Args:
        records: A list of record.
    """

    def __init__(self, records):
        self._records = records

    @property
    def count(self):
        return len(self._records)

    @property
    def total_defect(self):
        return sum(record.defect_count for record in self._records)

    @property
    def total_comment(self):
        return sum(record.comment_count for record in self._records)

    @property
    def total_loc(self):
        return sum(record.loc for record in self._records)

    @property
    def total_loc_changed(self):
        return sum(record.loc_changed for record in self._records)

    @property
    def total_person_time_in_second(self):
        return sum(
            record.total_person_time_in_second for record in self._records
        )

    @property
    def groupby_review_creation_month(self):
        return utils.groupby(self._records,
                             key=lambda record: record.review_creation_month)

    @property
    def groupby_review_creation_year(self):
        return utils.groupby(self._records,
                             key=lambda record: record.review_creation_year)

    @property
    def groupby_creator_login(self):
        return utils.groupby(self._records,
                             key=lambda record: record.creator_login)

    @property
    def groupby_creator_product_name(self):
        return utils.groupby(self._records,
                             key=lambda record: record.creator_product_name)

    @property
    def groupby_severity(self):
        return utils.groupby(self._records,
                             key=lambda record: record.severity)

    @property
    def groupby_type_cvb(self):
        return utils.groupby(self._records,
                             key=lambda record: record.type_cvb)

    @property
    def groupby_injection_stage(self):
        return utils.groupby(self._records,
                             key=lambda record: record.injection_stage)

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
