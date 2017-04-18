"""Records filter."""

from itertools import filterfalse


class ProductFilter:
    """Filter records by its product name.

    Args:
        records: A list of records, each record must have a
                 "creator_product_name" property.
        keywords: A list of filter keywords.
    Attributes:
        records: Data source to filter.
        keywords: Keywords of filter operation.
    Example:
        filter = CreatorFilter([Record(creator_product_name='foo')], ['foo'])
        filter.filter()
    """

    def __init__(self, records, keywords=None):
        self.records = records
        self.set_keywords(keywords)

    def set_keywords(self, keywords=None):
        """Setter for keywords."""
        if not keywords:
            keywords = []
        if not isinstance(keywords, list):
            keywords = [keywords]
        self.keywords = keywords

    def filter(self):
        """Filter function."""
        if not self.records:
            return self.records
        if not self.keywords:
            return self.records

        result_iterator = filterfalse(
            lambda record: not record.creator_product_name in self.keywords,
            self.records)
        return list(result_iterator)
