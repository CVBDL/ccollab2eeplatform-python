"""Define a review record."""

from ccollab2eeplatform.ccollab.record_field_index import review_field_index
from ccollab2eeplatform.settings.users_settings import UsersSettings


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
        """A string of review creaion date.

        Examples:
            "2017-01-09 15:59 UTC"
        """
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
        """Convert total person time to seconds.

        Available total person time formats:
            "1d, 07:55:04"
            "3:40:56"
            "0:03:55"
        """
        time_in_second = 0
        days_in_second = 0
        parts = self.total_person_time.split(',')
        time_parts = parts[-1].strip().split(':')
        time_in_second = (int(time_parts[0]) * 60 * 60
                          + int(time_parts[1]) * 60
                          + int(time_parts[2]))

        # Parse: "1d, 07:55:04".
        if len(parts) == 2:
            days = int((parts[0].strip())[:-1])
            days_in_second = days * 24 * 60 * 60

        return days_in_second + time_in_second

    @property
    def creator_product_name(self):
        return UsersSettings.get_product_by_login(self.creator_login)

    @property
    def review_creation_year(self):
        """Return a string for the year of review creation date"""
        return (self.review_creation_date)[0:4]

    @property
    def review_creation_month(self):
        """Return a string for the month of review creation date"""
        return (self.review_creation_date)[0:7]