"""Define a defect record."""

from ccollab2eeplatform.ccollab.record_field_index import DEFECT_FIELD_INDEX
from ccollab2eeplatform.settings.users_settings import UsersSettings


def lower(func):
    def _lower(*args, **kwargs):
        return str.lower(str.strip(func(*args, **kwargs)))
    return _lower


class DefectRecord():
    """Class for a defect record.

    Args:
        record: A string list contains some fields.
    """

    def __init__(self, record):
        self.record = record

    @property
    def defect_id(self):
        """Defect id."""
        return self.record[DEFECT_FIELD_INDEX['defect_id']]

    @property
    def review_id(self):
        """Review id."""
        return self.record[DEFECT_FIELD_INDEX['review_id']]

    @property
    def review_creation_date(self):
        """A string of review creaion date.

        Examples:
            "2017-01-09 15:59 UTC"
        """
        return self.record[DEFECT_FIELD_INDEX['review_creation_date']]

    @property
    def review_creation_year(self):
        """Year of review creation date.

        Returns:
            str: A year like "2017".
        """
        return (self.review_creation_date)[0:4]

    @property
    def review_creation_month(self):
        """Month of review creation date.

        Returns:
            str: A month like "2017-01".
        """
        return (self.review_creation_date)[0:7]


    @property
    def creator_login(self):
        """Creator login name."""
        return self.record[DEFECT_FIELD_INDEX['creator_login']]

    @property
    def creator_full_name(self):
        """Creator full name."""
        return self.record[DEFECT_FIELD_INDEX['creator_full_name']]

    @property
    def creator_product_name(self):
        """Creator product name.

        Returns:
            str: Product name like "ViewPoint".
        """
        return UsersSettings.get_product_by_login(self.creator_login)

    @property
    def severity(self):
        """Severity."""
        return self.record[DEFECT_FIELD_INDEX['severity']]

    @property
    def type_cvb(self):
        """Type CVB."""
        return self.record[DEFECT_FIELD_INDEX['type_cvb']]

    @property
    @lower
    def injection_stage(self):
        """Injection state."""
        return self.record[DEFECT_FIELD_INDEX['injection_stage']]
