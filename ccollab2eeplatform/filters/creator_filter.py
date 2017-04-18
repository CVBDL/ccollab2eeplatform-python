"""Records filter."""

from itertools import filterfalse


class CreatorFilter:
    """Filter records by its creator.

    Args:
        records: A list of records, each record must have a
                 "creator_login" property.
        keywords: A list of filter keywords.
    Attributes:
        records: Data source to filter.
        keywords: Keywords of filter operation.
    Example:
        filter = CreatorFilter([Record(creator_login='foo')], ['foo'])
        filter.filter()
        filter.filter(['bar'])
    """

    def __init__(self, records, keywords=None):
        self.records = records
        self.keywords = keywords

    def filter(self, keywords=None):
        """Filter records, and return the result.

        Args:
            keywords: A list of filter keywords.
        Returns:
            A list of records filter out by given keywords.
        Todo:
            Cache the result.
        """
        if self.records is None:
            return None

        # keywords from function parameter has a higher priority.
        if keywords is None:
            kws = self.keywords
        else:
            kws = keywords

        # If no keywords provided, then do nothing.
        if not kws:
            return self.records
        if not isinstance(kws, list):
            kws = [kws]
        result_iterator = filterfalse(
            lambda record: not record.creator_login in kws, self.records)
        return list(result_iterator)
