"""Records statistics module."""

from ccollab2eeplatform import utils


class RecordsStatistics:
    """Review records statistics class.

    Args:
        records: A list of record.
    """

    def __init__(self, records, start_date=None, end_date=None):
        self._records = records
        self._start_date = start_date
        self._end_date = end_date

    @property
    def count(self):
        """Records count."""
        return len(self._records)

    @property
    def total_defect(self):
        """Defects count."""
        return sum(record.defect_count for record in self._records)

    @property
    def total_comment(self):
        """Total comments."""
        return sum(record.comment_count for record in self._records)

    @property
    def total_loc(self):
        """Total LOC."""
        return sum(record.loc for record in self._records)

    @property
    def total_loc_changed(self):
        """Total LOC changed."""
        return sum(record.loc_changed for record in self._records)

    @property
    def total_person_time_in_second(self):
        """Total person time in second."""
        return sum(
            record.total_person_time_in_second for record in self._records
        )

    @property
    def groupby_review_creation_month(self):
        """Groupby review creation month."""
        return utils.groupby(self._records,
                             key=lambda record: record.review_creation_month)

    @property
    def groupby_review_creation_year(self):
        """Groupby review creation year."""
        return utils.groupby(self._records,
                             key=lambda record: record.review_creation_year)

    @property
    def groupby_creator_login(self):
        """Groupby creator login."""
        return utils.groupby(self._records,
                             key=lambda record: record.creator_login)

    @property
    def groupby_creator_product_name(self):
        """Groupby creator product name."""
        return utils.groupby(self._records,
                             key=lambda record: record.creator_product_name)

    @property
    def groupby_severity(self):
        """Groupby severity."""
        return utils.groupby(self._records,
                             key=lambda record: record.severity)

    @property
    def groupby_type_cvb(self):
        """Groupby type cvb."""
        return utils.groupby(self._records,
                             key=lambda record: record.type_cvb)

    @property
    def groupby_injection_stage(self):
        """Groupby injection stage."""
        return utils.groupby(self._records,
                             key=lambda record: record.injection_stage)

    @property
    def count_by_month(self):
        """Record count by month.

        Data table:
        Month    Count
        2016-01  20
        2016-03  10
        2016-05  25

        Returns:
            A tuple of column definition and data.
        """
        schema, data = [('Month', 'string'), ('Count', 'number')], []
        if self._start_date and self._end_date:
            stat = {}
            for key, group in self.groupby_review_creation_month:
                stat[key] = sum(1 for _ in group)
            month_range = utils.month_range(self._start_date, self._end_date)
            for month in month_range:
                data.append([month, stat.get(month, 0)])
        else:
            for key, group in self.groupby_review_creation_month:
                data.append([key, sum(1 for _ in group)])
        return schema, data

    @property
    def count_by_product(self):
        """Record count by product.

        Data table:
        Product  Count
        Team1    20
        Team2    16

        Returns:
            A tuple of column definition and data.
        """
        schema, data = [('Month', 'string'), ('Count', 'number')], []
        for key, group in self.groupby_creator_product_name:
            data.append([key, sum(1 for _ in group)])
        return schema, data
