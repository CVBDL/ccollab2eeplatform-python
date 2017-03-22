"""Define a review record."""

from ccollab2eeplatform.ccollab.record_field_index import review_field_index


class ReviewRecord():
    """Class for a review record.

    Args:
        record: A string list contains some fields.
    """
    def __init__(self, record):
        self.record = record

    @property
    def id(self):
        return self.record[review_field_index['id']]

    @property
    def review_creation_date(self):
        return self.record[review_field_index['review_creation_date']]

    @property
    def creator_login(self):
        return self.record[review_field_index['creator_login']]

    @property
    def creator(self):
        return self.record[review_field_index['creator_login']]

    @property
    def creator_full_name(self):
        return self.record[review_field_index['creator_full_name']]

    @property
    def defect_count(self):
        return self.record[review_field_index['defect_count']]

    @property
    def comment_count(self):
        return self.record[review_field_index['comment_count']]

    @property
    def loc(self):
        return self.record[review_field_index['loc']]

    @property
    def loc_changed(self):
        return self.record[review_field_index['loc_changed']]

    @property
    def total_person_time(self):
        return self.record[review_field_index['total_person_time']]

    @property
    def total_person_time_in_second(self):
        pass

    @property
    def creator_product_name(self):
        pass

    @property
    def review_creation_year(self):
        pass

    @property
    def review_creation_month(self):
        pass

    @property
    def review_creation_day(self):
        pass
