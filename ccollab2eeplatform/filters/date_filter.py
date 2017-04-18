"""Date filter for records."""

from itertools import filterfalse


class DateFilter:
    """Filter records by review creation date.

    Args:
        records: A list of records.
        keywords: A list of filter keywords.
        rule (str): Date string matching rule.
                    Could be 'year', 'month' or 'day'. Default: 'month'
    Attributes:
        records: Data source to filter.
        keywords: Keywords of filter operation.
        rule: Date string matching rule.
    Example:
        filter = DateFilter([Record], keywords='2017-01-01', rule='year')
        filter.filter()
    """

    rules = ('year', 'month', 'day')

    def __init__(self, records, keywords=None, rule=None):
        self.records = records if records else []
        self.set_keywords(keywords)
        self.set_rule(rule)

    def set_keywords(self, keywords=None):
        """Setter for keywords."""
        if keywords is None:
            keywords = []
        if not isinstance(keywords, list):
            keywords = [keywords]
        self.keywords = keywords

    def set_rule(self, rule=None):
        """Setter for rule."""
        if rule is None or str.lower(rule) not in self.rules:
            rule = self.rules[1]
        else:
            rule = str.lower(rule)
        self.rule = rule

    def _determine_keywords(self):
        kws = []
        for kw in self.keywords:
            if self.rule == self.rules[0]:
                kws.append(kw[0:4])
            elif self.rule == self.rules[1]:
                kws.append(kw[0:7])
            else:
                kws.append(kw)
        return kws

    def filter(self):
        """Filter function."""
        if not self.records:
            return self.records

        kws = self._determine_keywords()
        if not kws:
            return self.records

        def _filter(func):
            return filterfalse(func, self.records)

        if self.rule == self.rules[0]:
            result_iterator = _filter(
                lambda record: not record.review_creation_year in kws)
        elif self.rule == self.rules[1]:
            result_iterator = _filter(
                lambda record: not record.review_creation_month in kws)
        else:
            result_iterator = _filter(
                lambda record: not record.review_creation_day in kws)

        return list(result_iterator)
