"""Injection stage filter."""

from itertools import filterfalse


class InjectionStageFilter:
    """Filter records by "injection_stage" property.

    Args:
        records: A list of records to filter.
        keywords: Filter keywords.
                  For multiple keywords put them in a list.
    Attributes:
        records: The list of records to filter.
        keywords: Filter keywords list.
    Example:
        filter = InjectionStageFilter([Record], 'foo')
        filter = InjectionStageFilter([Record], ['foo', 'bar'])
        filter.set_keywords('foobar')
        filter.filter()
    """ 

    def __init__(self, records, keywords=None):
        if isinstance(records, list):
            self.records = records
        else:
            self.records = None
        self.set_keywords(keywords)

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

    def filter(self):
        """Filter function.
        
        Returns:
            Filtered records list.  None if error occurred.
            If keyword is None or empty list, then returns all records.
        """
        if not self.records or not self.keywords:
            return self.records
        try:
            result_iterator = filterfalse(
                lambda record: not record.injection_stage in self.keywords,
                self.records)
            return list(result_iterator)
        except AttributeError:
            return None
