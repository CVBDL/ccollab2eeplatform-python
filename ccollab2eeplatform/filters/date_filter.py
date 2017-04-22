"""Date filter."""

from itertools import filterfalse


class DateFilter:
    """Filter records by "review_creation_date" property.

    Args:
        records: A list of records to filter.
        keywords: Filter keywords.
                  For multiple keywords put them in a list.
        rule (str): Date string matching rule.
                    Could be 'year', 'month' or 'day'. Default: 'month'
    Attributes:
        records: The list of records to filter.
        keywords: Filter keywords list.
        rule: Date string matching rule.
    Example:
        filter = DateFilter([Record], keywords='2017-01-01', rule='year')
        filter.set_keywords('2017-02-01')
        filter.set_keywords('month')
        filter.filter()
    """

    rules = ('year', 'month', 'day')

    def __init__(self, records, keywords=None, rule=None):
        if isinstance(records, list):
            self.records = records
        else:
            self.records = None
        self.set_keywords(keywords)
        self.set_rule(rule)

    def set_keywords(self, keywords):
        """Setter for keywords."""
        if keywords is None:
            self.keywords = None
        else:
            self.keywords = []
            keywords = keywords if isinstance(keywords, list) else [keywords]
            for kw in keywords:
                if isinstance(kw, str):
                    self.keywords.append(str.lower(str.strip(kw)))
                else:
                    self.keywords.append(kw)

    def set_rule(self, rule):
        """Setter for rule."""
        if rule is None or str.lower(str.strip(rule)) not in self.rules:
            rule = self.rules[1]
        else:
            rule = str.lower(str.strip(rule))
        self.rule = rule

    def _determine_keywords(self):
        if self.keywords is None:
            return None
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
        kws = self._determine_keywords()
        if not self.records or not kws:
            return self.records

        def _filter(func):
            return filterfalse(func, self.records)

        try:
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
        except AttributeError:
            return None
